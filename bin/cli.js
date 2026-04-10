#!/usr/bin/env node

import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// path to python file
const pythonFile = path.join(__dirname, "../main.py");

const processRun = spawn("python", [pythonFile], {
  stdio: "inherit",
  shell: true
});

processRun.on("exit", (code) => {
  process.exit(code);
});
