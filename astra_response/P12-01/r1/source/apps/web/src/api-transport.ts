/** The only credential destination policy, shared by auth and business clients. */
const configuredProductionOrigin: unknown = import.meta.env.VITE_BVA_PRODUCTION_ORIGIN;

export function apiDestination(
  requestUrl: string,
  documentOrigin = window.location.origin,
  mode = import.meta.env.MODE,
  productionOrigin: string | undefined = typeof configuredProductionOrigin === 'string'
    ? configuredProductionOrigin
    : undefined,
): { url: string; credentials: RequestCredentials } {
  const qualificationApi =
    import.meta.env.MODE === 'android-qualification' ? 'https://localhost:18443' : undefined;
  const input = new URL(requestUrl);
  if (
    input.origin !== documentOrigin ||
    input.username ||
    input.password ||
    input.hash ||
    !input.pathname.startsWith('/api/')
  )
    throw new Error('Unapproved API destination');
  if (
    mode.startsWith('android-') &&
    !['android-qualification', 'android-production'].includes(mode)
  )
    throw new Error('Unapproved Android transport mode');
  const qualification = mode === 'android-qualification';
  const production = mode === 'android-production';
  if (qualification && documentOrigin !== 'https://localhost')
    throw new Error('Unapproved qualification document origin');
  if (qualification && qualificationApi === undefined)
    throw new Error('Qualification API is unavailable outside its TEST build');
  if (production) {
    if (
      productionOrigin === undefined ||
      !/^https:\/\/(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z](?:[a-z0-9-]*[a-z0-9])?$/.test(
        productionOrigin,
      ) ||
      productionOrigin.endsWith('.localhost') ||
      documentOrigin !== 'https://android.' + new URL(productionOrigin).hostname
    )
      throw new Error('Unapproved production Android origin');
  } else if (productionOrigin !== undefined) {
    throw new Error('Production Android origin outside production mode');
  }
  return {
    url:
      (qualification ? qualificationApi : production ? productionOrigin : documentOrigin) +
      input.pathname +
      input.search,
    credentials: qualification || production ? 'include' : 'same-origin',
  };
}

export function apiFetch(input: Request): Promise<Response> {
  const destination = apiDestination(input.url);
  const policy: RequestInit = {
    credentials: destination.credentials,
    cache: 'no-store',
    redirect: 'error',
  };
  if (destination.url === input.url) return fetch(new Request(input, policy));
  // Existing clients send bounded JSON, not streaming uploads. Passing Request.body
  // as a stream makes Chromium require HTTP/2 and breaks direct Uvicorn HTTP/1.1.
  const body = input.body === null ? Promise.resolve(null) : input.arrayBuffer();
  return body.then((bytes) =>
    fetch(
      new Request(destination.url, {
        method: input.method,
        headers: input.headers,
        body: bytes,
        signal: input.signal,
        ...policy,
      }),
    ),
  );
}
