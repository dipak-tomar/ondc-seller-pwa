import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { productsApi } from '@/lib/api';
import { Upload } from 'lucide-react';

interface CSVUploadProps {
  onSuccess: () => void;
}

export default function CSVUpload({ onSuccess }: CSVUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);

  const uploadMutation = useMutation({
    mutationFn: productsApi.bulkUpload,
    onSuccess: (response) => {
      setResult(response.data);
      if (response.data.errors.length === 0) {
        setTimeout(() => onSuccess(), 2000);
      }
    },
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
    }
  };

  const handleUpload = () => {
    if (file) {
      uploadMutation.mutate(file);
    }
  };

  return (
    <div className="space-y-4">
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="hidden"
          id="csv-upload"
        />
        <label htmlFor="csv-upload" className="cursor-pointer">
          <Button type="button" variant="outline" onClick={() => document.getElementById('csv-upload')?.click()}>
            Choose CSV File
          </Button>
        </label>
        {file && (
          <p className="mt-2 text-sm text-gray-600">
            Selected: {file.name}
          </p>
        )}
      </div>

      <div className="text-sm text-gray-600">
        <p className="font-medium mb-2">CSV Format:</p>
        <p>Required columns: name, price, mrp, stock</p>
        <p>Optional columns: description, sku, hsn_code, category</p>
        <p className="mt-2 text-xs">Maximum 1000 rows per upload</p>
      </div>

      {result && (
        <div className={`p-4 rounded ${result.errors.length > 0 ? 'bg-yellow-50' : 'bg-green-50'}`}>
          <p className="font-medium">
            {result.products_created} products uploaded successfully
          </p>
          {result.errors.length > 0 && (
            <div className="mt-2">
              <p className="text-sm font-medium text-red-600">Errors:</p>
              <ul className="text-sm text-red-600 list-disc list-inside">
                {result.errors.slice(0, 5).map((error: string, idx: number) => (
                  <li key={idx}>{error}</li>
                ))}
                {result.errors.length > 5 && (
                  <li>... and {result.errors.length - 5} more errors</li>
                )}
              </ul>
            </div>
          )}
        </div>
      )}

      <Button
        onClick={handleUpload}
        disabled={!file || uploadMutation.isPending}
        className="w-full"
      >
        {uploadMutation.isPending ? 'Uploading...' : 'Upload CSV'}
      </Button>
    </div>
  );
}
