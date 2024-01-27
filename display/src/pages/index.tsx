import Image from "next/image";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <>
      <div className="bg-slate-200 min-h-screen">
        <div className="flex justify-center">
          <div className="bg-slate-200 p-20">
            <h1 className="text-5xl">Rewind Pac Man!</h1>
          </div>
        </div>
        <div className="flex justify-center">
          <Image
            className="relative dark:drop-shadow-[0_0_0.3rem_#ffffff70] dark:invert"
            src="/pac-man-img.jpg"
            alt="Next.js Logo"
            width={180}
            height={40}
            priority
          />
        </div>
      </div>
    </>
  );
}
