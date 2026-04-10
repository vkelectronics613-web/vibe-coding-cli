#!/usr/bin/env node

const { execSync } = require("child_process");
const path = require("path");

const script = path.join(__dirname, "main.py");

try {
  execSync(`python "${script}"`, { stdio: "inherit" });
} catch (e) {
  console.error("❌ Failed to run AI CLI:", e.message);
}
