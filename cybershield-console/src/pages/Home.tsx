import { Link } from "react-router-dom";
import { Layout } from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Shield, Search, MessageCircle, BookOpen, FileText } from "lucide-react";

const features = [
  {
    icon: Search,
    title: "Scam Detection",
    description: "Analyze URLs, SMS, and messages for potential threats",
    path: "/scam-detection",
  },
  {
    icon: MessageCircle,
    title: "Victim Assistance",
    description: "Get help and guidance if you've been affected by cybercrime",
    path: "/victim-assistance",
  },
  {
    icon: BookOpen,
    title: "Awareness",
    description: "Learn about common cyber threats and how to protect yourself",
    path: "/awareness",
  },
  {
    icon: FileText,
    title: "Report Incident",
    description: "Submit a report about suspicious activity or cyber incidents",
    path: "/contact",
  },
];

export default function Home() {
  return (
    <Layout>
      {/* Hero Section */}
      <section className="py-16 md:py-24 bg-secondary">
        <div className="container">
          <div className="max-w-3xl mx-auto text-center">
            <div className="flex justify-center mb-6">
              <Shield className="h-16 w-16 text-primary" strokeWidth={1.5} />
            </div>
            <h1 className="text-3xl md:text-4xl lg:text-5xl font-semibold text-foreground mb-4">
              Your Trusted Partner in Cybersecurity
            </h1>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              CyberShield provides government-grade tools to detect scams, assist
              victims, and promote cyber safety awareness for citizens and
              organizations.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button asChild size="lg">
                <Link to="/scam-detection">Check for Scams</Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link to="/contact">Report an Incident</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="container">
          <h2 className="text-2xl md:text-3xl font-semibold text-foreground text-center mb-12">
            How We Can Help
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature) => (
              <Link key={feature.path} to={feature.path}>
                <Card className="h-full hover:bg-secondary/50 transition-colors cursor-pointer">
                  <CardHeader>
                    <feature.icon className="h-10 w-10 text-muted-foreground mb-2" strokeWidth={1.5} />
                    <CardTitle className="text-lg">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-sm">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="py-16 bg-secondary">
        <div className="container">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-2xl md:text-3xl font-semibold text-foreground mb-4">
              Trusted by Government & Public Safety Organizations
            </h2>
            <p className="text-muted-foreground">
              CyberShield is designed to meet the security and compliance
              standards required by law enforcement agencies, regulatory bodies,
              and government institutions. Our platform prioritizes data privacy,
              accessibility, and user trust.
            </p>
          </div>
        </div>
      </section>
    </Layout>
  );
}
