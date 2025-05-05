const ReportViewer = ({ report }) => (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Damage Report</h2>
      <p className="whitespace-pre-line">{report}</p>
    </div>
  );
  
  export default ReportViewer;
  