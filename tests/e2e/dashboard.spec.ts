import { test, expect } from '@playwright/test';

test.describe('AuraTorrent Demo Flow', () => {
  test('should load the application correctly', async ({ page }) => {
    // Navigate to the app
    await page.goto('/');

    // Ensure the main Vue container is rendered
    const appContainer = page.locator('#app');
    await expect(appContainer).toBeVisible();

    // Ensure Vuetify application class is attached
    const vApp = page.locator('.v-application');
    await expect(vApp).toBeVisible();
  });
});
