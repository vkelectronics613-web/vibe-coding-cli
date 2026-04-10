#!/usr/bin/env node
"use strict";

const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const mainPy = path.join(__dirname, "main.py");

if (!fs.existsSync(mainPy)) {
  console.error("❌ Fatal: main.py not found at", mainPy);
  process.exit(1);
}

// Try python3 first (Linux/macOS), fall back to python (Windows)
const pythonCmd = process.platform === "win32" ? "python" : "python3";

const child = spawn(pythonCmd, [mainPy], {
  stdio: "inherit",
  cwd: process.cwd(),
  env: { ...process.env },
});

child.on("error", (err) => {
  if (err.code === "ENOENT") {
    // python3 not found on non-Windows, try python
    const fallback = spawn("python", [mainPy], {
      stdio: "inherit",
      cwd: process.cwd(),
      env: { ...process.env },
    });
    fallback.on("error", () => {
      console.error("❌ Python is not installed or not in PATH.");
      console.error("   Install Python 3.8+ from https://python.org");
      process.exit(1);
    });
    fallback.on("exit", (code) => process.exit(code ?? 0));
  } else {
    console.error("❌ Failed to start:", err.message);
    process.exit(1);
  }
});

child.on("exit", (code) => process.exit(code ?? 0));
