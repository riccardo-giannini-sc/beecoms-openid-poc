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
        // $oldheaders = array($request->headers->all())[0];
        $headers = [];

        if ($request->bearerToken()) {
            $headers['Authorization'] = "Bearer "  . $request->bearerToken();
        }


        // foreach ($oldheaders as $i => $h) {
        //     $headers[ucwords($i)] = ucwords($h[0]);
        // }
        
        // try {
            $client = new Client();
            $response = $client->request($method, $this->receiver_url . '/' . $endpoint, [
                    'headers' => array_merge($headers, $additional_headers),
                    'body' => $request->getContent(),
                    'allow_redirects' => ['strict' => true],
                    'http_errors' => false,
                    // 'debug' => true,
            ]);

            if ($response->getStatusCode() !== 200) {
                return Response::json(['foo' => 'bar'], 403);
                return response()->json($response->getBody()->getContents(), $response->getStatusCode());
            }
        // } catch (ClientException $ex) {
            
            // if ($ex->hasResponse()) {
                // dd($ex);
                // $response = $ex->getResponse();
                // return response()->json($response->getBody(), $response->getStatusCode());
            // }
        // }

        return $response;
    }

    public function auth_code(Request $request)
    {
        $additional_headers = [
            'content-type' => "application/x-www-form-urlencoded",
            'cache-control' => "no-cache"
        ];
        $this->forward_request('POST', 'o/token/', $request, $additional_headers);
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
