"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, Save, Play, Users } from "lucide-react";

export default function CampaignEditor({ params }: { params: { id: string } }) {
  const isNew = params.id === "new";
  const [name, setName] = useState(isNew ? "New Campaign" : "Sample Campaign");
  const [subject, setSubject] = useState("Hello {{first_name}}!");
  const [body, setBody] = useState("Hi {{first_name}},\n\nI noticed you work at {{company}}. We have a great product for you.\n\nBest,\nSales Team");

  return (
    <div className="max-w-5xl mx-auto pb-12">
      <div className="flex items-center mb-6 text-sm text-gray-500">
        <Link href="/campaigns" className="hover:text-blue-600 flex items-center">
          <ArrowLeft className="h-4 w-4 mr-1" />
          Back to Campaigns
        </Link>
      </div>

      <div className="flex justify-between items-end mb-6">
        <div className="flex-1">
          <label className="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-1">Campaign Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="text-3xl font-bold text-gray-900 bg-transparent border-none p-0 focus:ring-0 outline-none w-full"
          />
        </div>
        <div className="flex space-x-3">
          <button className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none">
            <Save className="mr-2 h-4 w-4 text-gray-500" />
            Save Draft
          </button>
          <button className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none">
            <Play className="mr-2 h-4 w-4" />
            Start Campaign
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Editor Area */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Email Template</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Subject Line</label>
                <input
                  type="text"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="E.g., Great news for {{company}}"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email Body</label>
                <textarea
                  rows={12}
                  value={body}
                  onChange={(e) => setBody(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm font-mono"
                  placeholder="Write your email here. Use {{variable}} for personalization."
                />
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar / Contacts */}
        <div className="space-y-6">
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Recipients</h3>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                0 Contacts
              </span>
            </div>
            
            <p className="text-sm text-gray-500 mb-4">
              Upload a CSV file containing your contacts. The column headers will be available as variables in your email template.
            </p>
            
            <button className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none">
              <Users className="mr-2 h-4 w-4 text-gray-500" />
              Manage Contacts
            </button>
            
            <div className="mt-6">
              <h4 className="text-sm font-medium text-gray-900 mb-2">Available Variables</h4>
              <div className="flex flex-wrap gap-2">
                <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800 font-mono">
                  {'{{first_name}}'}
                </span>
                <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800 font-mono">
                  {'{{company}}'}
                </span>
                <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800 font-mono">
                  {'{{email}}'}
                </span>
              </div>
              <p className="text-xs text-gray-500 mt-2">Variables are extracted from your CSV headers automatically.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
