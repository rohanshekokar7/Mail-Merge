import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Mail, LayoutDashboard, Settings, Users, LogOut } from "lucide-react";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Mail Merge Platform",
  description: "Production-quality web-based Mail Merge Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex h-screen bg-gray-50">
          {/* Sidebar */}
          <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
            <div className="h-16 flex items-center px-6 border-b border-gray-200">
              <Mail className="h-6 w-6 text-blue-600 mr-2" />
              <span className="font-bold text-lg text-gray-900">MailMerge</span>
            </div>
            
            <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
              <Link href="/" className="flex items-center px-3 py-2 text-sm font-medium rounded-md bg-blue-50 text-blue-700">
                <LayoutDashboard className="h-5 w-5 mr-3" />
                Dashboard
              </Link>
              <Link href="/campaigns" className="flex items-center px-3 py-2 text-sm font-medium rounded-md text-gray-700 hover:bg-gray-100">
                <Mail className="h-5 w-5 mr-3" />
                Campaigns
              </Link>
              <Link href="/contacts" className="flex items-center px-3 py-2 text-sm font-medium rounded-md text-gray-700 hover:bg-gray-100">
                <Users className="h-5 w-5 mr-3" />
                Contacts
              </Link>
              <Link href="/settings" className="flex items-center px-3 py-2 text-sm font-medium rounded-md text-gray-700 hover:bg-gray-100">
                <Settings className="h-5 w-5 mr-3" />
                Settings
              </Link>
            </nav>
            
            <div className="p-4 border-t border-gray-200">
              <button className="flex items-center w-full px-3 py-2 text-sm font-medium rounded-md text-gray-700 hover:bg-gray-100">
                <LogOut className="h-5 w-5 mr-3" />
                Log out
              </button>
            </div>
          </aside>

          {/* Main Content Area */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Top Navigation */}
            <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
              <h1 className="text-xl font-semibold text-gray-800">Welcome</h1>
              <div className="flex items-center space-x-4">
                <div className="h-8 w-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-semibold">
                  A
                </div>
              </div>
            </header>

            {/* Page Content */}
            <main className="flex-1 overflow-y-auto p-6">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
