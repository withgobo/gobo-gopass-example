import { STATUS_CODES } from "node:http";

export function notFoundHandler(req, res) {
  res.status(404);
  res.render("error.html", {
    code: 404,
    status: STATUS_CODES[404],
    message: `The requested URL ${req.originalUrl} was not found on this server.`,
  });
}

export function errorHandler(err, req, res, next) {
  if (res.headersSent) {
    return next(err);
  }

  let code;
  if (err) {
    if (
      typeof err.status === "number" &&
      err.status >= 400 &&
      err.status < 600
    ) {
      code = err.status;
    } else if (
      typeof err.statusCode === "number" &&
      err.statusCode >= 400 &&
      err.statusCode < 600
    ) {
      code = err.statusCode;
    } else {
      code = res.statusCode;
      if (typeof code !== "number" || code < 400 || code >= 600) {
        code = 500;
      }
    }
  }

  let message = err.message;
  if (code >= 500) {
    message = "";
    console.error(err.stack || err.toString());
  }

  res.status(code);
  res.render("error.html", {
    code: code,
    status: STATUS_CODES[code],
    message: message,
  });
}
