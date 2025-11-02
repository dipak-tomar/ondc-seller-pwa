import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { CheckCircle2, Circle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface ChecklistItem {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  route?: string;
}

export function OnboardingChecklist() {
  const navigate = useNavigate();
  const [items, setItems] = useState<ChecklistItem[]>([
    {
      id: 'profile',
      title: 'Complete your profile',
      description: 'Add your store name and contact details',
      completed: false,
      route: '/settings'
    },
    {
      id: 'product',
      title: 'Add your first product',
      description: 'Create a product or upload via CSV',
      completed: false,
      route: '/products'
    },
    {
      id: 'images',
      title: 'Upload product images',
      description: 'Add high-quality images to your products',
      completed: false,
      route: '/products'
    },
    {
      id: 'sync',
      title: 'Sync to ONDC',
      description: 'Make your products available on ONDC network',
      completed: false,
      route: '/products'
    }
  ]);

  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    const savedState = localStorage.getItem('onboarding-checklist');
    if (savedState) {
      const parsed = JSON.parse(savedState);
      setItems(parsed.items);
      setDismissed(parsed.dismissed);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('onboarding-checklist', JSON.stringify({ items, dismissed }));
  }, [items, dismissed]);

  const toggleItem = (id: string) => {
    setItems(items.map(item => 
      item.id === id ? { ...item, completed: !item.completed } : item
    ));
  };

  const handleItemClick = (item: ChecklistItem) => {
    if (item.route) {
      navigate(item.route);
    }
  };

  const completedCount = items.filter(item => item.completed).length;
  const allCompleted = completedCount === items.length;

  if (dismissed || allCompleted) {
    return null;
  }

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Getting Started</span>
          <span className="text-sm font-normal text-muted-foreground">
            {completedCount} / {items.length} completed
          </span>
        </CardTitle>
        <CardDescription>
          Complete these steps to get your store ready
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {items.map(item => (
          <div
            key={item.id}
            className="flex items-start gap-3 p-3 rounded-lg hover:bg-accent cursor-pointer transition-colors"
            onClick={() => handleItemClick(item)}
          >
            <Checkbox
              checked={item.completed}
              onCheckedChange={() => toggleItem(item.id)}
              onClick={(e) => e.stopPropagation()}
            />
            <div className="flex-1">
              <div className="flex items-center gap-2">
                {item.completed ? (
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                ) : (
                  <Circle className="h-4 w-4 text-muted-foreground" />
                )}
                <h4 className={`font-medium ${item.completed ? 'line-through text-muted-foreground' : ''}`}>
                  {item.title}
                </h4>
              </div>
              <p className="text-sm text-muted-foreground mt-1">
                {item.description}
              </p>
            </div>
          </div>
        ))}
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setDismissed(true)}
          className="w-full"
        >
          Dismiss
        </Button>
      </CardContent>
    </Card>
  );
}
