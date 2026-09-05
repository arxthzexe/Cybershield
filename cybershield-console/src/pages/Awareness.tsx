import { Layout } from "@/components/Layout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { 
  Mail, 
  Lock, 
  Smartphone, 
  CreditCard, 
  Users, 
  Globe, 
  ShieldAlert, 
  Key 
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

interface AwarenessCard {
  icon: LucideIcon;
  title: string;
  description: string;
  tips: string[];
}

const awarenessCards: AwarenessCard[] = [
  {
    icon: Mail,
    title: "Phishing Attacks",
    description: "Learn to identify fraudulent emails and messages designed to steal your information.",
    tips: [
      "Check sender email addresses carefully",
      "Never click suspicious links",
      "Verify requests through official channels",
      "Look for grammar and spelling errors",
    ],
  },
  {
    icon: Lock,
    title: "Password Security",
    description: "Strong passwords are your first line of defense against unauthorized access.",
    tips: [
      "Use unique passwords for each account",
      "Enable two-factor authentication",
      "Use a password manager",
      "Avoid personal information in passwords",
    ],
  },
  {
    icon: Smartphone,
    title: "Mobile Security",
    description: "Protect your smartphone from malware and unauthorized access.",
    tips: [
      "Keep your OS and apps updated",
      "Only download from official stores",
      "Be cautious with app permissions",
      "Use screen lock and biometrics",
    ],
  },
  {
    icon: CreditCard,
    title: "Financial Fraud",
    description: "Recognize and prevent common financial scams and fraud attempts.",
    tips: [
      "Monitor bank statements regularly",
      "Never share OTPs or PINs",
      "Use secure payment methods",
      "Be wary of 'too good to be true' offers",
    ],
  },
  {
    icon: Users,
    title: "Social Engineering",
    description: "Understand manipulation tactics used by scammers to gain your trust.",
    tips: [
      "Verify identities before sharing info",
      "Be skeptical of urgent requests",
      "Don't let emotions drive decisions",
      "Confirm requests through known contacts",
    ],
  },
  {
    icon: Globe,
    title: "Safe Browsing",
    description: "Navigate the internet safely and protect your online privacy.",
    tips: [
      "Look for HTTPS in website URLs",
      "Avoid public Wi-Fi for sensitive tasks",
      "Keep browser and plugins updated",
      "Use reputable security software",
    ],
  },
  {
    icon: ShieldAlert,
    title: "Ransomware",
    description: "Protect against malware that can lock your files and demand payment.",
    tips: [
      "Regularly backup important data",
      "Don't open unexpected attachments",
      "Keep software up to date",
      "Never pay ransom demands",
    ],
  },
  {
    icon: Key,
    title: "Identity Protection",
    description: "Safeguard your personal information from identity thieves.",
    tips: [
      "Limit personal info shared online",
      "Shred sensitive documents",
      "Review credit reports regularly",
      "Use identity theft protection services",
    ],
  },
];

export default function Awareness() {
  return (
    <Layout>
      <div className="container py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-3xl font-semibold text-foreground mb-2">
            Cyber Safety Awareness
          </h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Knowledge is your best defense. Learn about common cyber threats and
            how to protect yourself, your family, and your organization.
          </p>
        </div>

        {/* Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {awarenessCards.map((card) => (
            <Card key={card.title} className="h-full">
              <CardHeader>
                <card.icon className="h-8 w-8 text-muted-foreground mb-2" strokeWidth={1.5} />
                <CardTitle className="text-lg">{card.title}</CardTitle>
                <CardDescription className="text-sm">
                  {card.description}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {card.tips.map((tip, index) => (
                    <li
                      key={index}
                      className="flex items-start gap-2 text-sm text-muted-foreground"
                    >
                      <span className="text-primary">•</span>
                      {tip}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Additional Resources */}
        <div className="mt-16 text-center">
          <h2 className="text-2xl font-semibold text-foreground mb-4">
            Stay Informed
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Cyber threats evolve constantly. Stay updated by regularly checking
            official government cybersecurity advisories and subscribing to
            trusted security newsletters.
          </p>
        </div>
      </div>
    </Layout>
  );
}
