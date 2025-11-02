import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Button } from '@/components/ui/button';
import { HelpCircle, ExternalLink, Mail } from 'lucide-react';

export function HelpSection() {
  const faqs = [
    {
      question: 'How do I add products?',
      answer: 'You can add products manually by clicking "Add Product" on the Products page, or upload multiple products at once using a CSV file. The CSV should include columns for name, description, SKU, HSN code, price, MRP, stock, and category.'
    },
    {
      question: 'What is ONDC sync?',
      answer: 'ONDC sync publishes your products to the Open Network for Digital Commerce, making them available to buyers across multiple platforms. Click "Sync to ONDC" on the Products page to sync your catalog.'
    },
    {
      question: 'How do I manage inventory?',
      answer: 'Go to the Inventory page to view current stock levels. You can adjust inventory by clicking on a product and entering the quantity change with a reason (e.g., "Restock", "Damaged", "Sold").'
    },
    {
      question: 'What image requirements should I follow?',
      answer: 'Product images should be at least 800x800 pixels and under 2MB in size. Use clear, high-quality photos with good lighting. You can upload multiple images per product.'
    },
    {
      question: 'How do I confirm orders?',
      answer: 'Orders appear on the Orders page. Click "Confirm" to accept an order, which will automatically update your inventory and send a notification to the customer.'
    },
    {
      question: 'What are pricing rules?',
      answer: 'Pricing rules let you set up automatic discounts based on conditions like bulk purchases or specific categories. Create rules in the Settings page under Pricing Rules.'
    }
  ];

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <HelpCircle className="h-5 w-5" />
            Help & Documentation
          </CardTitle>
          <CardDescription>
            Find answers to common questions and learn how to use the platform
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Accordion type="single" collapsible className="w-full">
            {faqs.map((faq, index) => (
              <AccordionItem key={index} value={`item-${index}`}>
                <AccordionTrigger>{faq.question}</AccordionTrigger>
                <AccordionContent>{faq.answer}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Resources</CardTitle>
          <CardDescription>
            Additional documentation and support
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <Button variant="outline" className="w-full justify-between" asChild>
            <a href="https://docs.ondc.org" target="_blank" rel="noopener noreferrer">
              ONDC Documentation
              <ExternalLink className="h-4 w-4" />
            </a>
          </Button>
          <Button variant="outline" className="w-full justify-between" asChild>
            <a href="/docs/api-contract.md" target="_blank" rel="noopener noreferrer">
              API Documentation
              <ExternalLink className="h-4 w-4" />
            </a>
          </Button>
          <Button variant="outline" className="w-full justify-between" asChild>
            <a href="mailto:support@ondcseller.com">
              Contact Support
              <Mail className="h-4 w-4" />
            </a>
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Quick Tips</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p>• Use high-quality images to increase sales</p>
          <p>• Keep your inventory updated to avoid overselling</p>
          <p>• Respond to orders quickly to maintain good ratings</p>
          <p>• Use bulk upload for adding many products at once</p>
          <p>• Enable notifications to stay updated on new orders</p>
        </CardContent>
      </Card>
    </div>
  );
}
