
import { test, expect } from '@playwright/test'

test.describe('Visual Testing with Percy', () => {
  test('Homepage visual test', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveScreenshot('homepage.png')
  })
  
  test('Dashboard visual test', async ({ page }) => {
    await page.goto('/dashboard')
    await expect(page).toHaveScreenshot('dashboard.png')
  })
  
  test('Agent cards visual test', async ({ page }) => {
    await page.goto('/agents')
    await expect(page).toHaveScreenshot('agent-cards.png')
  })
})
