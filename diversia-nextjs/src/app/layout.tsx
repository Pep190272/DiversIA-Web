import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DiversIA - Plataforma de Inclusión Laboral",
  description: "Conectamos talento neurodivergente con empresas inclusivas",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body>
        {children}
      </body>
    </html>
  );
}