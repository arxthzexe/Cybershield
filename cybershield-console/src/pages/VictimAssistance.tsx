import { useState } from "react";
import { Layout } from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Shield, Send, User } from "lucide-react";

interface Message {
  id: number;
  type: "user" | "assistant";
  content: string;
}

// Backend API replaces faqDatabase

export default function VictimAssistance() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: "assistant",
      content: "Hello! I'm the CyberShield Assistant. I'm here to help you if you've been affected by cybercrime or need guidance on staying safe online.\n\nHow can I assist you today?",
    },
  ]);
  const [inputValue, setInputValue] = useState("");

  const handleSend = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: messages.length + 1,
      type: "user",
      content: inputValue,
    };

    setMessages([...messages, userMessage]);
    setInputValue("");

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: inputValue })
      });
      const data = await res.json();
      
      const assistantMessage: Message = {
        id: messages.length + 2,
        type: "assistant",
        content: data.response || "I am currently unavailable.",
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (e) {
      console.error(e);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Layout>
      <div className="container py-12">
        <div className="max-w-3xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-semibold text-foreground mb-2">
              Victim Assistance
            </h1>
            <p className="text-muted-foreground">
              Get help and guidance if you've been affected by cybercrime. Our
              assistant is here to support you.
            </p>
          </div>

          {/* Chat Interface */}
          <Card className="h-[600px] flex flex-col">
            {/* Chat Header */}
            <div className="border-b border-border p-4 flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-secondary flex items-center justify-center">
                <Shield className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground">
                  CyberShield Assistant
                </p>
                <p className="text-xs text-muted-foreground">
                  Here to help you stay safe
                </p>
              </div>
            </div>

            {/* Messages */}
            <ScrollArea className="flex-1 p-4">
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex gap-3 ${
                      message.type === "user" ? "flex-row-reverse" : ""
                    }`}
                  >
                    <div
                      className={`h-8 w-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                        message.type === "user"
                          ? "bg-primary"
                          : "bg-secondary"
                      }`}
                    >
                      {message.type === "user" ? (
                        <User className="h-4 w-4 text-primary-foreground" />
                      ) : (
                        <Shield className="h-4 w-4 text-primary" />
                      )}
                    </div>
                    <div
                      className={`max-w-[80%] rounded-lg p-3 ${
                        message.type === "user"
                          ? "bg-primary text-primary-foreground"
                          : "bg-secondary text-secondary-foreground"
                      }`}
                    >
                      <p className="text-sm whitespace-pre-line">
                        {message.content}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>

            {/* Input */}
            <div className="border-t border-border p-4">
              <div className="flex gap-2">
                <Input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type your message..."
                  className="flex-1"
                />
                <Button onClick={handleSend} disabled={!inputValue.trim()}>
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              <p className="text-xs text-muted-foreground mt-2 text-center">
                This is an automated assistant. For emergencies, contact your
                local authorities.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </Layout>
  );
}
