import { NextRequest, NextResponse } from "next/server";

let startTime: number | null = null;

export async function POST(req: NextRequest) {
    startTime = Date.now();
    return NextResponse.json({message: "START TIME SAVED: ", startTime})
}

export async function GET(req: NextRequest) {
    if ( startTime === null) {
        return NextResponse.json({message: "START TIME NOT SET!"})
    }
    return NextResponse.json({startTime})
}