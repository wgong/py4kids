terms_table_str = """

<table>
    <tr align=left> 
        <th>Name </th> 
        <th>Description </th> 
    </tr>
    <tr align=left> 
        <td>OpenID Provider (OP) 
        </td> 
        <td>an OAuth 2.0 server that is capable of authenticating the end-user and providing information about the result of the authentication and the end-user to the Relying Party 
        </td>
    </tr>
    <tr align=left> 
        <td>Relying Party (RP) 
        </td> 
        <td>an OAuth 2.0 application that “relies” on the OP to handle authentication requests 
        </td>
    </tr>
    <tr align=left> 
        <td>Resource Owner 
        </td> 
        <td>You are the owner of your identity, your data, and any actions that can be performed with your accounts 
        </td>
    </tr>
    <tr align=left> 
        <td>Client
        </td> 
        <td>The application (e.g. “Terrible Pun of the Day”) that wants to access data or perform actions on behalf of the Resource Owner
        </td>
    </tr>
    <tr align=left> 
        <td>Authorization Server
        </td> 
        <td>The application that knows the Resource Owner, where the Resource Owner already has an account
        </td>
    </tr>
    <tr align=left> 
        <td>Resource Server
        </td> 
        <td>The Application Programming Interface (API) or service the Client wants to use on behalf of the Resource Owner
        </td>
    </tr>
    
<tr align=left>
	<td>Redirect URI
	</td>
	<td>The URL the Authorization Server will redirect the Resource Owner back to after granting permission to the Client. This is sometimes referred to as the “Callback URL.”
	</td>
</tr>
<tr align=left>
	<td>Response Type
	</td>
	<td>The type of information the Client expects to receive. The most common Response Type is code, where the Client expects an Authorization Code.
	</td>
</tr>
<tr align=left>
	<td>Scope
	</td>
	<td>These are the granular permissions the Client wants, such as access to data or to perform actions.
	</td>
</tr>
<tr align=left>
	<td>Consent
	</td>
	<td>The Authorization Server takes the Scopes the Client is requesting, and verifies with the Resource Owner whether or not they want to give the Client permission.
	</td>
</tr>
<tr align=left>
	<td>Client ID
	</td>
	<td>This ID is used to identify the Client with the Authorization Server.
	</td>
</tr>
<tr align=left>
	<td>Client Secret
	</td>
	<td>This is a secret password that only the Client and Authorization Server know. This allows them to securely share information privately behind the scenes.
	</td>
</tr>
<tr align=left>
	<td>Authorization Code
	</td>
	<td>A short-lived temporary code the Client gives the Authorization Server in exchange for an Access Token.
	</td>
</tr>
<tr align=left>
	<td>Access Token
	</td>
	<td>The key the client will use to communicate with the Resource Server. This is like a badge or key card that gives the Client permission to request data or perform actions with the Resource Server on your behalf.
	</td>
</tr>    
</table>

"""


endpoints_table_str = """
<table>
    <tr align=left> 
        <th>Endpoint </th> 
        <th>Description </th> 
    </tr>
    <tr align=left> 
        <td>/authorization 
        </td> 
        <td>Typically, you kick off an OIDC interaction by hitting an <em>/authorization</em> endpoint with an HTTP GET. A number of query parameters indicate what you can expect to get back after authenticating and what you’ll have access to (authorization) 
        </td>
    </tr>
    <tr align=left> 
        <td>/token 
        </td> 
        <td>Often, you’ll need to hit a <em>/token</em> endpoint with an HTTP POST to get tokens which are used for further interactions
        </td>
    </tr>
    <tr align=left> 
        <td>/introspect 
        </td> 
        <td>OIDC also has an <em>/introspect</em> endpoint for verifying a token
        </td>
    </tr>
    <tr align=left> 
        <td>/userinfo 
        </td> 
        <td>OIDC also has an <em>/userinfo</em> endpoint for for getting identity information about the user.
        </td>
    </tr>
    <tr align=left> 
        <td>metadata 
        </td> 
        <td>One of the great improvements in OIDC is a <em>metadata</em> mechanism to discover endpoints from the provider. For instance, if you navigate to: https://micah.okta.com/oauth2/aus2yrcz7aMrmDAKZ1t7/.well-known/openid-configuration, you’ll get back a JSON formatted document with the metadata that identifies all the available endpoints from the OP (Okta, in this case)
        </td>
    </tr>

</table>

"""


scope_table_str = """
<table>
    <tr align=left> 
        <th>Scope </th> 
        <th>Purpose </th> 
    </tr>
    <tr align=left> 
        <td>openid
        </td> 
        <td>required scope for ID 
        </td>
    </tr>
    <tr align=left> 
        <td>profile
        </td> 
        <td>requests access to default profile claims
        </td>
    </tr>
    <tr align=left> 
        <td>email
        </td> 
        <td>requests access to email and email_verified claims
        </td>
    </tr>
    <tr align=left> 
        <td>address
        </td> 
        <td>requests access to address claim
        </td>
    </tr>

    <tr align=left> 
        <td>address
        </td> 
        <td>requests access to address claim
        </td>
    </tr>


</table>

"""


flow_table_str = """
<table>
    <tr align=left> 
        <th>Flow </th> 
        <th>Authentication & Authorization Scenario </th> 
    </tr>
    <tr align=left> 
        <td>Authorization Code
        </td> 
        <td><em>response_type=code</em>. After successful authentication, the response will contain a <em>code</em> value. This code can later be exchanged for an <em>access_token</em> and an <em>id_token</em>.
         This flow is useful where you have “middleware” as part of the architecture. The middleware has a <em>client_id</em> and <em>client_secret</em>, which is required to exchange the code for <em>tokens</em> by hitting the <em>/token</em> endpoint. These <em>tokens</em> can then be returned to the end-user application, such as a browser, without the browser ever having to know the <em>client_secret</em>. This flow allows for long-lived sessions through the use of <em>refresh_tokens</em>. The only purpose of <em>refresh_token</em> is to obtain new <em>access_tokens</em> to extend a user session.
        </td>
    </tr>
    <tr align=left> 
        <td>Implicit
        </td> 
        <td><em>response_type=id_token token</em> or <em>response_type=id_token</em>.
        After successful authentication, the response will contain an <em>id_token</em> and an <em>access_token</em> in the first case or just an <em>id_token</em> in the second case. This flow is useful when you have an app speaking directly to a backend to obtain tokens with no middleware. It does not support long-lived sessions.
        </td>
    </tr>
    <tr align=left> 
        <td>Hybrid
        </td> 
        <td>This flow combines the above two in different combinations – whatever make sense for the use case. An example would be <em>response_type=code id_token</em>. This approach enables a scenario whereby you can have a long lived session in an app and get tokens back immediately from the <em>/authorization</em> endpoint
        </td>
    </tr>

    <tr align=left> 
        <td>Client Credentials Grant
        </td> 
        <td>The client can request an access token using only its client
   credentials (or other supported means of authentication) when the
   client is requesting access to the protected resources under its
   control, or those of another resource owner that have been previously
   arranged with the authorization server
        </td>
    </tr>

    <tr align=left> 
        <td>Resource Owner Password Credentials Grant
        </td> 
        <td>suitable in
   cases where the resource owner has a trust relationship with the
   client, such as the device operating system or a highly privileged application.  The authorization server should take special care when enabling this grant type and only allow it when other flows are not
   viable
        </td>
    </tr>


</table>
"""


token_table_str = """
<table>
    <tr align=left> 
        <th>Token </th> 
        <th>Description </th> 
    </tr>
    <tr align=left> 
        <td>id_token
        </td> 
        <td>ID tokens carry identity information encoded in the token itself, which must be a JWT. It has 3 parts: header, body, signing.
        </td>
    </tr>
    <tr align=left> 
        <td>access_token
        </td> 
        <td>Access tokens are used to gain access to resources by using them as bearer tokens. 
        It is shorted lived with expires.
        </td>
    </tr>
    <tr align=left> 
        <td>refresh_token
        </td> 
        <td>Refresh tokens exist solely to get more access tokens. It is long-lived.
        </td>
    </tr>


</table>

"""