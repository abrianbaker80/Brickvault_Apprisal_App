import { expect, it } from 'vitest';
import { capacitorConfig } from '../../android/capacitor.config';

it('retains the localhost TEST WebView configuration outside production', () => {
  expect(capacitorConfig({}).server).toEqual({
    hostname: 'localhost',
    androidScheme: 'https',
    cleartext: false,
  });
  expect(() =>
    capacitorConfig({ BVA_ANDROID_PRODUCTION_ORIGIN: 'https://app.example.test' }),
  ).toThrow();
});

it('requires an exact production HTTPS API origin and bundled same-site WebView', () => {
  expect(
    capacitorConfig({
      BVA_ANDROID_MODE: 'production',
      BVA_ANDROID_PRODUCTION_ORIGIN: 'https://app.example.test',
    }).server,
  ).toEqual({
    hostname: 'android.app.example.test',
    androidScheme: 'https',
    cleartext: false,
  });
  for (const origin of [
    undefined,
    'http://app.example.test',
    'https://localhost',
    'https://localhost:18443',
    'https://app.localhost',
    'https://127.0.0.1',
    'https://app.example.test:443',
    'https://app.example.test/path',
    'https://*.example.test',
  ]) {
    expect(() =>
      capacitorConfig({ BVA_ANDROID_MODE: 'production', BVA_ANDROID_PRODUCTION_ORIGIN: origin }),
    ).toThrow();
  }
});
