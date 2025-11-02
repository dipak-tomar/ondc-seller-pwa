import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { authApi } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';
import { Mail, Phone } from 'lucide-react';

export default function AuthPage() {
  const [step, setStep] = useState<'input' | 'verify'>('input');
  const [method, setMethod] = useState<'email' | 'phone'>('email');
  const [contact, setContact] = useState('');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();
  const { setToken, setUser } = useAuthStore();

  const handleRequestOTP = async () => {
    setLoading(true);
    setError('');
    try {
      const data = method === 'email' ? { email: contact } : { phone: contact };
      await authApi.requestOTP(data);
      setStep('verify');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to send OTP');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async () => {
    setLoading(true);
    setError('');
    try {
      const data = method === 'email' 
        ? { email: contact, otp } 
        : { phone: contact, otp };
      const response = await authApi.verifyOTP(data);
      setToken(response.data.access_token);
      
      const userResponse = await authApi.getMe();
      setUser(userResponse.data);
      
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid OTP');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl">ONDC Seller Booster</CardTitle>
          <CardDescription>
            {step === 'input' ? 'Sign in to your account' : 'Enter the OTP sent to you'}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {step === 'input' ? (
            <>
              <div className="flex gap-2">
                <Button
                  variant={method === 'email' ? 'default' : 'outline'}
                  onClick={() => setMethod('email')}
                  className="flex-1"
                >
                  <Mail className="w-4 h-4 mr-2" />
                  Email
                </Button>
                <Button
                  variant={method === 'phone' ? 'default' : 'outline'}
                  onClick={() => setMethod('phone')}
                  className="flex-1"
                >
                  <Phone className="w-4 h-4 mr-2" />
                  Phone
                </Button>
              </div>
              
              <Input
                type={method === 'email' ? 'email' : 'tel'}
                placeholder={method === 'email' ? 'Enter your email' : 'Enter your phone'}
                value={contact}
                onChange={(e) => setContact(e.target.value)}
              />
              
              {error && <p className="text-sm text-red-500">{error}</p>}
              
              <Button 
                onClick={handleRequestOTP} 
                disabled={loading || !contact}
                className="w-full"
              >
                {loading ? 'Sending...' : 'Send OTP'}
              </Button>
            </>
          ) : (
            <>
              <p className="text-sm text-gray-600">
                OTP sent to {contact}
              </p>
              
              <Input
                type="text"
                placeholder="Enter 6-digit OTP"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                maxLength={6}
              />
              
              {error && <p className="text-sm text-red-500">{error}</p>}
              
              <div className="flex gap-2">
                <Button 
                  variant="outline"
                  onClick={() => setStep('input')}
                  className="flex-1"
                >
                  Back
                </Button>
                <Button 
                  onClick={handleVerifyOTP} 
                  disabled={loading || otp.length !== 6}
                  className="flex-1"
                >
                  {loading ? 'Verifying...' : 'Verify'}
                </Button>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
