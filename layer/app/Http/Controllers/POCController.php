<?php

namespace App\Http\Controllers;

use GuzzleHttp\Client;
use Illuminate\Http\Request;

class POCController extends Controller
{
    private $receiver_url = "http://prm:8000";

    private function forward_request(string $method, string $endpoint, Request $request, array $additional_headers = [])
    {
        // $oldheaders = array($request->headers->all())[0];
        $headers = [];

        if ($request->bearerToken()) {
            $headers['Authorization'] = "Bearer "  . $request->bearerToken();
        }


        // foreach ($oldheaders as $i => $h) {
        //     $headers[ucwords($i)] = ucwords($h[0]);
        // }

        $client = new Client();
        $response = $client->request($method, $this->receiver_url . '/' . $endpoint, [
                'headers' => array_merge($headers, $additional_headers),
                'body' => $request->getContent(),
                'allow_redirects' => ['strict' => true],
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
        $this->forward_request('POST', 'token', $request, $additional_headers);
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
