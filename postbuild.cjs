const fs = require('fs')
const path = require('path')

function createVersionFile() {
  const packageJson = require('./package.json')
  const version = packageJson.version

  const dirPath = path.join(__dirname, 'auratorrent')
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true })
  }

  const filePath = path.join(dirPath, 'version.txt')
  fs.writeFileSync(filePath, version)
}

createVersionFile()
