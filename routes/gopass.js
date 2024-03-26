import express from "express";
import createError from "http-errors";
import jsonwebtoken from "jsonwebtoken";
import nocache from "nocache";
import { URL } from "node:url";

const router = express.Router();

// User/org being logged into your Gobo marketplace. We're hardcoding
// the values here, but this would typically be from a database lookup.
const USER_INFO = {
  user_id: "user_123",
  user_email: "john@example.com",
  user_firstname: "John",
  user_lastname: "Doe",
  org_id: "org_13",
  org_name: "Org 123",
  role: "admin",
};

router.get("/", nocache(), (req, res, next) => {
  // Make sure the required environment variables are set.
  if (!process.env.GOPASS_KEY || !process.env.GOPASS_URL) {
    return res.status(500).render("error.html", {
      title: "Error",
      message: "Please check your GoPass configuration.",
    });
  }

  // Don't allow logging into the wrong organization.
  if (req.query.target || req.query.target_id) {
    if (req.query.target_id !== USER_INFO.org_id) {
      return next(
        createError(403, "User is not a member of this organization."),
      );
    }
  }

  // Create and sign the JWT.
  const claims = {
    ver: "1.0",
    iat: Math.floor(Date.now() / 1000), // issued at time
    ...USER_INFO,
  };
  const jwt = jsonwebtoken.sign(claims, process.env.GOPASS_KEY);
  const url = new URL(jwt, process.env.GOPASS_URL);

  // Redirect the user to the GoPass login URL.
  console.log(`Redirecting to: ${url.href}`);
  return res.redirect(url);
});

export default router;
