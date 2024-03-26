import express from "express";
import morgan from "morgan";
import nunjucks from "nunjucks";

import { errorHandler, notFoundHandler } from "./lib/error.js";
import gopassRouter from "./routes/gopass.js";
import indexRouter from "./routes/index.js";

const app = express();
const port = process.env.PORT || 8300;

// templates
nunjucks.configure("templates", {
  autoescape: true,
  express: app,
});

// logging
app.use(morgan("dev"));

// routes
app.use("/", indexRouter);
app.use("/gopass", gopassRouter);

// error pages
app.use(notFoundHandler);
app.use(errorHandler);

// server
app.listen(port, () => {
  console.log(`Listening on http://localhost:${port}`);
});
