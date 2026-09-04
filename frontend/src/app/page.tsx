export default function Home() {
  return (
    <div className="max-w-4xl">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Dashboard (Phase 1 Placeholder)</h2>
        <p className="text-gray-600 mb-6">
          The frontend application is successfully connected and running.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
            <h3 className="text-sm font-medium text-blue-800">Total Campaigns</h3>
            <p className="mt-2 text-3xl font-semibold text-blue-900">0</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg border border-green-100">
            <h3 className="text-sm font-medium text-green-800">Emails Sent</h3>
            <p className="mt-2 text-3xl font-semibold text-green-900">0</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg border border-purple-100">
            <h3 className="text-sm font-medium text-purple-800">Open Rate</h3>
            <p className="mt-2 text-3xl font-semibold text-purple-900">0%</p>
          </div>
        </div>
      </div>
    </div>
  );
}
