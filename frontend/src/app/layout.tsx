import type { Metadata } from "next";
import Script from "next/script";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "Task Board - Hackathon 2",
  description: "Manage your tasks with a beautiful glassmorphism interface",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <Script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          strategy="afterInteractive"
        />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Space+Grotesk:wght@500;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased">
        {children}
        <ToastContainer
          position="top-right"
          autoClose={2800}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          pauseOnFocusLoss={false}
          draggable
          pauseOnHover
          theme="dark"
        />
      </body>
    </html>
  );
}
