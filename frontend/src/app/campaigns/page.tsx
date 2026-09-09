import Link from "next/link";
import { PlusCircle, Mail, Clock, PlayCircle, CheckCircle, FileEdit, Trash2 } from "lucide-react";

export default function CampaignsPage() {
  // In a real app, this would be fetched from the backend API
  const campaigns = [
    { id: 1, name: "Welcome Series", status: "RUNNING", sent: 150, total: 200, openRate: "45%" },
    { id: 2, name: "Q3 Newsletter", status: "DRAFT", sent: 0, total: 500, openRate: "0%" },
    { id: 3, name: "Product Update", status: "COMPLETED", sent: 1200, total: 1200, openRate: "62%" },
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "RUNNING":
        return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"><PlayCircle className="w-3 h-3 mr-1"/> Running</span>;
      case "DRAFT":
        return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"><FileEdit className="w-3 h-3 mr-1"/> Draft</span>;
      case "COMPLETED":
        return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"><CheckCircle className="w-3 h-3 mr-1"/> Completed</span>;
      default:
        return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">{status}</span>;
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Campaigns</h2>
          <p className="text-sm text-gray-500">Manage your email campaigns and view their performance.</p>
        </div>
        <Link 
          href="/campaigns/new"
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <PlusCircle className="mr-2 h-5 w-5" />
          Create Campaign
        </Link>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {campaigns.map((campaign) => (
            <li key={campaign.id}>
              <div className="px-4 py-4 sm:px-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex flex-col">
                    <Link href={`/campaigns/${campaign.id}`} className="text-lg font-medium text-blue-600 hover:text-blue-800 truncate">
                      {campaign.name}
                    </Link>
                    <div className="mt-2 flex items-center text-sm text-gray-500">
                      <Mail className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                      <p>
                        {campaign.sent} / {campaign.total} emails sent
                      </p>
                    </div>
                  </div>
                  <div className="flex flex-col items-end space-y-2">
                    {getStatusBadge(campaign.status)}
                    <div className="text-sm text-gray-500 font-medium">
                      Open Rate: {campaign.openRate}
                    </div>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
