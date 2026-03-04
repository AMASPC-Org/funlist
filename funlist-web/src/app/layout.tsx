import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "FunList.ai - Discover Family-Friendly Events",
  description: "Curated events, family-friendly picks, and your saved favorites all in one warm spot.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {/* Main Navigation Bar */}
        <nav className="navbar">
          <div className="container d-flex justify-content-between align-items-center flex-wrap">
            {/* Logo/Brand */}
            <Link href="/" className="navbar-brand">
              <span>FunList.ai</span>
            </Link>

            {/* Main Navigation Links */}
            <div className="d-flex align-items-center flex-wrap">
              <ul className="navbar-nav">
                <li>
                  <Link href="/map" className="nav-link">Map</Link>
                </li>
                <li>
                  <Link href="/events" className="nav-link">Events</Link>
                </li>
                <li>
                  <Link href="/auth/signin" className="nav-link">Add Event</Link>
                </li>
              </ul>

              {/* Login/Signup */}
              <div className="d-flex align-items-center" style={{ marginLeft: '2rem', gap: '0.5rem' }}>
                <Link href="/auth/signin" className="btn btn-sm btn-outline-primary">Login</Link>
                <Link href="/auth/signup" className="btn btn-sm btn-primary">Sign Up</Link>
              </div>
            </div>
          </div>
        </nav>

        <main role="main" className="mt-2" style={{ paddingBottom: '3rem', minHeight: 'calc(100vh - 400px)' }}>
          {children}
        </main>

        <footer className="footer mt-5 py-4">
          <div className="container">
            <div className="row">
              <div className="col-lg col-md-3 col-sm-6 mb-4">
                <h5 className="mb-3">COMPANY</h5>
                <ul className="list-unstyled mb-0">
                  <li className="mb-2"><Link href="/about">About Us</Link></li>
                  <li className="mb-2"><Link href="/contact">Contact</Link></li>
                  <li className="mb-2"><Link href="/help">Help Center</Link></li>
                  <li className="mb-2"><Link href="/advertising">Advertise with Us</Link></li>
                </ul>
              </div>
              <div className="col-lg col-md-3 col-sm-6 mb-4">
                <h5 className="mb-3">ACCOUNT</h5>
                <ul className="list-unstyled mb-0">
                  <li className="mb-2"><Link href="/auth/signin">Sign In</Link></li>
                  <li className="mb-2"><Link href="/auth/signup">Sign Up</Link></li>
                  <li className="mb-2"><Link href="/auth/signin">Add Event</Link></li>
                </ul>
              </div>
              <div className="col-lg col-md-3 col-sm-6 mb-4">
                <h5 className="mb-3">LEGAL</h5>
                <ul className="list-unstyled mb-0">
                  <li className="mb-2"><Link href="/terms">Terms & Conditions</Link></li>
                  <li className="mb-2"><Link href="/privacy">Privacy Policy</Link></li>
                </ul>
              </div>
              <div className="col-lg col-md-3 col-sm-6 mb-4">
                <h5 className="mb-3">NETWORK</h5>
                <ul className="list-unstyled mb-0">
                  <li className="mb-2"><a href="https://amaspc.com" target="_blank" rel="noreferrer">American Marketing Alliance SPC</a></li>
                  <li className="mb-2"><a href="https://businesscalendar.ai" target="_blank" rel="noreferrer">BusinessCalendar.ai</a></li>
                  <li className="mb-2"><a href="https://localmarketingtool.ai" target="_blank" rel="noreferrer">LocalMarketingTool.ai</a></li>
                  <li className="mb-2"><a href="https://thurstonai.com" target="_blank" rel="noreferrer">ThurstonAI</a></li>
                </ul>
              </div>
            </div>

            <hr className="my-3" style={{ opacity: 0.1, borderColor: 'var(--text-navy)' }} />
            <div className="row">
              <div className="col text-center">
                <p className="mb-0 text-muted" style={{ fontSize: '0.9rem' }}>
                  © 2026 FunList.ai. All rights reserved | Brought to you by <a href="https://americanmarketingalliance.com" target="_blank" rel="noreferrer">American Marketing Alliance SPC</a>
                </p>
              </div>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
