const { chromium } = require('@playwright/test');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

async function capture() {
  console.log('Starting Playwright...');
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    colorScheme: 'dark'
  });
  
  const page = await context.newPage();
  const url = 'http://127.0.0.1:5174/';
  
  console.log(`Navigating to ${url}...`);
  try {
    await page.goto(url, { waitUntil: 'networkidle' });
  } catch(e) {
    console.log('Failed to reach dev server. Make sure npx vite -m demo is running on port 5174.');
    process.exit(1);
  }

  const outDir = path.join(__dirname, '../docs/screenshots');
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  console.log('Capturing Dashboard...');
  await page.waitForTimeout(2000); 
  await page.screenshot({ path: path.join(outDir, 'frame01.png') });

  console.log('Opening Menu/Dropdown...');
  const menuBtn = await page.$('.v-select');
  if (menuBtn) await menuBtn.click();
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(outDir, 'frame02.png') });
  
  if (menuBtn) await menuBtn.click();
  await page.waitForTimeout(1000);

  console.log('Capturing Sidebar Hover...');
  await page.mouse.move(100, 200);
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, 'frame03.png') });

  await browser.close();
  
  console.log('Generating GIF using Playwright FFmpeg...');
  // Find ffmpeg from playwright installation
  const localAppData = process.env.LOCALAPPDATA;
  const pwPath = path.join(localAppData, 'ms-playwright');
  const dirs = fs.readdirSync(pwPath).filter(d => d.startsWith('ffmpeg-'));
  if (dirs.length > 0) {
    const ffmpegExe = path.join(pwPath, dirs[0], 'ffmpeg-win64.exe');
    
    if (fs.existsSync(ffmpegExe)) {
      const outGif = 'demo-loop.gif';
      if (fs.existsSync(path.join(outDir, outGif))) fs.unlinkSync(path.join(outDir, outGif));
      
      const cmd = `"${ffmpegExe}" -y -framerate 1 -i "frame%02d.png" -vf "scale=1280:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 "${outGif}"`;
      console.log('Running: ' + cmd);
      execSync(cmd, { cwd: outDir });
      console.log('GIF generated successfully at docs/screenshots/demo-loop.gif!');
    } else {
      console.log('FFmpeg executable not found in ms-playwright. Saving PNGs only.');
    }
  }
}

capture().catch(console.error);
