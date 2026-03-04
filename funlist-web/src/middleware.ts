import { NextRequest, NextResponse } from "next/server";
import { authMiddleware } from "next-firebase-auth-edge";

export async function middleware(request: NextRequest) {
  return authMiddleware(request, {
    loginPath: "/api/login",
    logoutPath: "/api/logout",
    apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY || "dummy",
    cookieName: "AuthToken",
    cookieSignatureKeys: ["secret1", "secret2"],
    cookieSerializeOptions: {
      path: "/",
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax" as const,
      maxAge: 12 * 60 * 60 * 24, // 12 days
    },
    serviceAccount: {
      projectId: process.env.FIREBASE_PROJECT_ID || "dummy",
      clientEmail: process.env.FIREBASE_CLIENT_EMAIL || "dummy",
      privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, "\n") || "dummy",
    },
    handleValidToken: async (_payload, headers) => {
      // Allow the request to proceed if valid
      return NextResponse.next({
        request: {
          headers
        }
      });
    },
    handleInvalidToken: async (reason) => {
      console.warn("Invalid token:", reason);
      const publicPaths = ["/", "/auth/signin", "/events"];
      if (publicPaths.includes(request.nextUrl.pathname)) {
        return NextResponse.next();
      }
      return NextResponse.redirect(new URL("/auth/signin", request.url));
    },
    handleError: async (error) => {
      console.error("Auth middleware error:", error);
      const publicPaths = ["/", "/auth/signin", "/events"];
      if (publicPaths.includes(request.nextUrl.pathname)) {
        return NextResponse.next();
      }
      return NextResponse.redirect(new URL("/auth/signin", request.url));
    }
  });
}

export const config = {
  matcher: [
    "/api/login",
    "/api/logout",
    "/",
    "/((?!_next|favicon.ico|api|.*\\.).*)",
  ],
};
