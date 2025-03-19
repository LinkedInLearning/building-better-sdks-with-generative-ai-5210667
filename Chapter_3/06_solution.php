<?php

/**
 * Twilio Messaging API Client
 *
 * This class provides methods to interact with the Twilio Messaging API.
 *
 * @category  API
 * @package   TwilioMessagingAPI
 * @license   https://opensource.org/licenses/MIT MIT License
 * @link      https://www.twilio.com/docs/sms
 */

class TwilioMessagingAPI
{
    private $accountSid;
    private $authToken;
    private $baseUrl;
    private $headers;

    /**
     * Constructor
     *
     * @param string $accountSid Account SID
     * @param string $authToken  Auth Token
     */
    public function __construct($accountSid, $authToken)
    {
        $this->accountSid = $accountSid;
        $this->authToken = $authToken;
        $this->baseUrl = "https://api.twilio.com/2010-04-01/Accounts/{$this->accountSid}";
        $this->headers = [
            "Authorization: Basic " . base64_encode("{$this->accountSid}:{$this->authToken}"),
            "Content-Type: application/x-www-form-urlencoded"
        ];
    }

    /**
     * Make an HTTP request
     *
     * @param string $method HTTP method (GET, POST, etc.)
     * @param string $url    URL for the request
     * @param array  $data   Data to send with the request
     *
     * @return array JSON response
     * @throws Exception If an HTTP error occurs
     */
    private function request($method, $url, $data = null)
    {
        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $this->headers);

        if ($data) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
        }

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

        if ($httpCode >= 400) {
            throw new Exception("HTTP Error: $httpCode - Response: $response");
        }

        curl_close($ch);

        return json_decode($response, true);
    }

    /**
     * Send an SMS message
     *
     * @param string $to   The destination phone number
     * @param string $from The phone number to send the message from
     * @param string $body The body of the message
     *
     * @return array The response from the API
     * @throws Exception If an HTTP error occurs
     */
    public function sendMessage($to, $from, $body)
    {
        $url = "{$this->baseUrl}/Messages.json";
        $data = [
            'To' => $to,
            'From' => $from,
            'Body' => $body
        ];

        return $this->request("POST", $url, $data);
    }

    /**
     * Fetch a message
     *
     * @param string $messageSid The SID of the message to fetch
     *
     * @return array The response from the API
     * @throws Exception If an HTTP error occurs
     */
    public function fetchMessage($messageSid)
    {
        $url = "{$this->baseUrl}/Messages/{$messageSid}.json";

        return $this->request("GET", $url);
    }

    /**
     * List messages
     *
     * @param array $params Optional parameters for filtering the list
     *
     * @return array The response from the API
     * @throws Exception If an HTTP error occurs
     */
    public function listMessages($params = [])
    {
        $url = "{$this->baseUrl}/Messages.json";

        if (!empty($params)) {
            $url .= '?' . http_build_query($params);
        }

        return $this->request("GET", $url);
    }
}

// Example usage:
$accountSid = "your_account_sid";
$authToken = "your_auth_token";
$twilio = new TwilioMessagingAPI($accountSid, $authToken);

try {
    // Send an SMS message
    $response = $twilio->sendMessage("+1234567890", "+0987654321", "Hello, World!");
    print_r($response);

    // Fetch a message
    $message = $twilio->fetchMessage("SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX");
    print_r($message);

    // List messages
    $messages = $twilio->listMessages(['PageSize' => 20]);
    print_r($messages);
} catch (Exception $e) {
    echo 'Error: ' . $e->getMessage();
}