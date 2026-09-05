import { Shield } from "lucide-react";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-background">
      <div className="container py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          {/* Logo and Name */}
          <div className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-muted-foreground" strokeWidth={1.5} />
            <span className="text-sm font-medium text-muted-foreground">
              CyberShield
            </span>
          </div>

          {/* Legal Disclaimer */}
          <p className="text-xs text-muted-foreground text-center max-w-xl">
            This platform is provided for informational purposes only. CyberShield
            does not guarantee the accuracy of scam detection results. Always
            exercise caution and report suspicious activities to appropriate
            authorities.
          </p>

          {/* Copyright */}
          <p className="text-xs text-muted-foreground">
            © {currentYear} CyberShield. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
