import { useState } from "react";
import { Layout } from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { RiskBadge } from "@/components/RiskBadge";
import { Search, AlertCircle, CheckCircle, Info } from "lucide-react";

type RiskLevel = "low" | "medium" | "high" | null;

interface ScanResult {
  risk: RiskLevel;
  explanation: string;
  recommendations: string[];
}

// We use backend API now

export default function ScamDetection() {
  const [urlInput, setUrlInput] = useState("");
  const [messageInput, setMessageInput] = useState("");
  const [result, setResult] = useState<ScanResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalyze = async (content: string, type: 'url' | 'message') => {
    setIsAnalyzing(true);
    try {
      const res = await fetch("http://localhost:8000/api/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type, content })
      });
      const data = await res.json();
      if (!data.error) {
        setResult(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getRiskIcon = (risk: RiskLevel) => {
    switch (risk) {
      case "high":
        return <AlertCircle className="h-6 w-6 text-destructive" />;
      case "medium":
        return <Info className="h-6 w-6 text-warning" />;
      case "low":
        return <CheckCircle className="h-6 w-6 text-success" />;
      default:
        return null;
    }
  };

  return (
    <Layout>
      <div className="container py-12">
        <div className="max-w-3xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-semibold text-foreground mb-2">
              Scam Detection
            </h1>
            <p className="text-muted-foreground">
              Analyze suspicious URLs, SMS messages, or emails to identify potential
              scams and threats.
            </p>
          </div>

          {/* Input Tabs */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="text-lg">Enter Content to Analyze</CardTitle>
              <CardDescription>
                Choose the type of content you want to scan for potential threats
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="url" className="w-full">
                <TabsList className="grid w-full grid-cols-2 mb-4">
                  <TabsTrigger value="url">URL</TabsTrigger>
                  <TabsTrigger value="message">SMS / Message</TabsTrigger>
                </TabsList>
                <TabsContent value="url">
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="url-input">Website URL</Label>
                      <Input
                        id="url-input"
                        type="url"
                        placeholder="https://example.com"
                        value={urlInput}
                        onChange={(e) => setUrlInput(e.target.value)}
                        className="mt-1"
                      />
                    </div>
                    <Button
                      onClick={() => handleAnalyze(urlInput, 'url')}
                      disabled={!urlInput.trim() || isAnalyzing}
                      className="w-full"
                    >
                      <Search className="h-4 w-4 mr-2" />
                      {isAnalyzing ? "Analyzing..." : "Analyze URL"}
                    </Button>
                  </div>
                </TabsContent>
                <TabsContent value="message">
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="message-input">Message Content</Label>
                      <Textarea
                        id="message-input"
                        placeholder="Paste the suspicious SMS or email content here..."
                        value={messageInput}
                        onChange={(e) => setMessageInput(e.target.value)}
                        rows={5}
                        className="mt-1"
                      />
                    </div>
                    <Button
                      onClick={() => handleAnalyze(messageInput, 'message')}
                      disabled={!messageInput.trim() || isAnalyzing}
                      className="w-full"
                    >
                      <Search className="h-4 w-4 mr-2" />
                      {isAnalyzing ? "Analyzing..." : "Analyze Message"}
                    </Button>
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          {/* Results */}
          {result && (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">Analysis Result</CardTitle>
                  {result.risk && <RiskBadge level={result.risk} />}
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-start gap-4">
                  {getRiskIcon(result.risk)}
                  <p className="text-sm text-muted-foreground">
                    {result.explanation}
                  </p>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-foreground mb-3">
                    Recommended Actions
                  </h4>
                  <ul className="space-y-2">
                    {result.recommendations.map((rec, index) => (
                      <li
                        key={index}
                        className="flex items-start gap-2 text-sm text-muted-foreground"
                      >
                        <span className="text-muted-foreground">•</span>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </Layout>
  );
}
