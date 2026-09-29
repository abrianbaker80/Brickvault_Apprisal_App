import type { CapacitorConfig } from '@capacitor/cli';

const LOCAL_SERVER = {
  hostname: 'localhost',
  androidScheme: 'https',
  cleartext: false,
} as const;

/** The network API origin is also the parent of the bundled WebView origin. */
export function productionAndroidOrigin(value: string | undefined): string {
  if (
    value === undefined ||
    !/^https:\/\/(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z](?:[a-z0-9-]*[a-z0-9])?$/.test(value) ||
    value.endsWith('.localhost')
  ) {
    throw new Error('Invalid production Android HTTPS origin');
  }
  return value;
}

export function capacitorConfig(environment: NodeJS.ProcessEnv): CapacitorConfig {
  const mode = environment.BVA_ANDROID_MODE;
  if (mode !== undefined && mode !== 'production') {
    throw new Error('Invalid Android configuration mode');
  }
  if (mode !== 'production' && environment.BVA_ANDROID_PRODUCTION_ORIGIN !== undefined) {
    throw new Error('Production Android origin requires production mode');
  }
  const server =
    mode === 'production'
      ? {
          ...LOCAL_SERVER,
          hostname:
            'android.' +
            new URL(productionAndroidOrigin(environment.BVA_ANDROID_PRODUCTION_ORIGIN)).hostname,
        }
      : LOCAL_SERVER;
  return {
    appId: 'com.abrianbaker.brickvault.appraisal',
    appName: 'BrickVault Appraisal App',
    webDir: '../web/dist',
    loggingBehavior: 'none',
    server,
    android: { allowMixedContent: false },
    plugins: {
      CapacitorHttp: { enabled: false },
      CapacitorCookies: { enabled: false },
      App: { disableBackButtonHandler: true },
    },
  };
}

export default capacitorConfig(process.env);
