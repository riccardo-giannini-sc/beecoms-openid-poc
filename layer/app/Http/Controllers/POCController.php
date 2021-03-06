<?php

namespace App\Http\Controllers;

use GuzzleHttp\Client;
use GuzzleHttp\Exception\ClientException;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Response;

class POCController extends Controller
{
    private $receiver_url = "http://prm:8000";

    private function forward_request(string $method, string $endpoint, Request $request, array $additional_headers = [])
    {
        $headers = [];

        if ($request->bearerToken()) {
            $headers['Authorization'] = "Bearer "  . $request->bearerToken();
        }

        $client = new Client();
        $response = $client->request($method, $this->receiver_url . '/' . $endpoint, [
                'headers' => array_merge($headers, $additional_headers),
                'body' => $request->getContent(),
                'allow_redirects' => ['strict' => true],
                'http_errors' => false,
                // 'debug' => true,
        ]);

        return $response;
    }

    public function auth_code(Request $request)
    {
        $additional_headers = [
            'content-type' => "application/x-www-form-urlencoded",
            'cache-control' => "no-cache"
        ];
        return $this->forward_request('POST', 'o/token/', $request, $additional_headers);
    }

    public function resource(Request $request)
    {
        return $this->forward_request('GET', 'resource/', $request);

    }

    public function refresh_token(Request $request)
    {
        return $this->forward_request('POST', '', $request);
    }

    public function revoke_token(Request $request)
    {
        return $this->forward_request('POST', '', $request);
    }
}
