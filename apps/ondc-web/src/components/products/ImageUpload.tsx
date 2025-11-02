import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Upload, X, Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface ImageUploadProps {
  productId: string;
  onUploadComplete?: (imageUrl: string) => void;
}

export function ImageUpload({ productId, onUploadComplete }: ImageUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const { toast } = useToast();

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    if (file.size > 2 * 1024 * 1024) {
      toast({
        title: 'File too large',
        description: 'Image must be under 2MB',
        variant: 'destructive'
      });
      return;
    }

    const img = new Image();
    const objectUrl = URL.createObjectURL(file);
    
    img.onload = async () => {
      if (img.width < 800 || img.height < 800) {
        toast({
          title: 'Image too small',
          description: 'Image must be at least 800x800 pixels',
          variant: 'destructive'
        });
        URL.revokeObjectURL(objectUrl);
        return;
      }

      setPreview(objectUrl);
      setUploading(true);

      try {
        const formData = new FormData();
        formData.append('file', file);

        const token = localStorage.getItem('token');
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/images/products/${productId}/upload`,
          {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`
            },
            body: formData
          }
        );

        if (!response.ok) {
          throw new Error('Upload failed');
        }

        const data = await response.json();
        
        toast({
          title: 'Success',
          description: 'Image uploaded successfully'
        });

        if (onUploadComplete) {
          onUploadComplete(data.image_url);
        }
      } catch (error) {
        toast({
          title: 'Upload failed',
          description: 'Failed to upload image. Please try again.',
          variant: 'destructive'
        });
        setPreview(null);
      } finally {
        setUploading(false);
        URL.revokeObjectURL(objectUrl);
      }
    };

    img.src = objectUrl;
  }, [productId, onUploadComplete, toast]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.webp']
    },
    maxFiles: 1,
    disabled: uploading
  });

  const clearPreview = () => {
    setPreview(null);
  };

  return (
    <Card className="p-6">
      {preview ? (
        <div className="relative">
          <img
            src={preview}
            alt="Preview"
            className="w-full h-64 object-cover rounded-lg"
          />
          {!uploading && (
            <Button
              variant="destructive"
              size="icon"
              className="absolute top-2 right-2"
              onClick={clearPreview}
            >
              <X className="h-4 w-4" />
            </Button>
          )}
          {uploading && (
            <div className="absolute inset-0 bg-black/50 flex items-center justify-center rounded-lg">
              <Loader2 className="h-8 w-8 text-white animate-spin" />
            </div>
          )}
        </div>
      ) : (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragActive ? 'border-primary bg-primary/5' : 'border-muted-foreground/25'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
          {isDragActive ? (
            <p className="text-lg">Drop the image here...</p>
          ) : (
            <>
              <p className="text-lg mb-2">Drag & drop an image here</p>
              <p className="text-sm text-muted-foreground mb-4">
                or click to select a file
              </p>
              <p className="text-xs text-muted-foreground">
                PNG, JPG, JPEG, or WEBP • Min 800x800px • Max 2MB
              </p>
            </>
          )}
        </div>
      )}
    </Card>
  );
}
