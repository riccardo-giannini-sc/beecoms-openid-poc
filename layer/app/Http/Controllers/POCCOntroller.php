<?php

namespace App\Http\Controllers;

use GuzzleHttp\Client;
use Illuminate\Http\Request;

class POCCOntroller extends Controller
{
    private $receiver_url = "http://127.0.0.1:8002";

    private function forward_request(string $method, string $endpoint, Request $request)
    {
        $client = new Client();
            $response = $client->request($method, $this->receiver_url . '/' . $endpoint, [
                'headers' => $request->get_headers(),
                'body' => $request->getContent(),
                'allow_redirects' => ['strict' => true],
                // 'debug' => true,
            ]);

        return $response;
    }

    public function auth_code(Request $request)
    {
        $this->forward_request('POST', 'token', $request);
    }

    public function resource(Request $request)
    {
        return $this->forward_request('GET', '', $request);
        
    }

    public function refresh_token(Request $request)
    {
        return $this->forward_request('POST', '', $request);
    }
}
