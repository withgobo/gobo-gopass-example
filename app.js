import express from "express";
import morgan from "morgan";
import nocache from "nocache";
import nunjucks from "nunjucks";

import { errorHandler, notFoundHandler } from "./lib/error.js";
import { gopassView } from "./views/gopass.js";
import { indexView } from "./views/index.js";

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
app.get("/", indexView);
app.get("/gopass", nocache(), gopassView);

// error pages
app.use(notFoundHandler);
app.use(errorHandler);

// server
app.listen(port, () => {
  console.log(`Listening on http://localhost:${port}`);
});
