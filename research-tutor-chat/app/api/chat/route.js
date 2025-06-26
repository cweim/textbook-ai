// app/api/chat/route.js
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

export async function POST(request) {
  try {
    const { message } = await request.json();

    if (!message || message.trim() === '') {
      return Response.json(
        { error: 'Message cannot be empty' },
        { status: 400 }
      );
    }

    // Path to your Python script
    const pythonScriptPath = path.join(process.cwd(), 'backend', 'tutor_api.py');

    // Execute Python script with the message as argument
    const command = `python "${pythonScriptPath}" "${message.replace(/"/g, '\\"')}"`;

    console.log('Executing:', command);

    const { stdout, stderr } = await execAsync(command);

    if (stderr) {
      console.error('Python script error:', stderr);
      return Response.json(
        { error: 'Error processing request' },
        { status: 500 }
      );
    }

    // Parse the JSON response from Python
    const result = JSON.parse(stdout);

    if (!result.success) {
      return Response.json(
        { error: result.error || 'Unknown error occurred' },
        { status: 500 }
      );
    }

    return Response.json({
      response: result.response,
      tokensUsed: result.tokens_used
    });

  } catch (error) {
    console.error('API Error:', error);
    return Response.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Handle CORS for development
export async function OPTIONS(request) {
  return new Response(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}
