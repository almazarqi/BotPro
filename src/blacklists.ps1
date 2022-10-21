param (
  [string]$ip = $(throw "ip is required.")
 )

$httpBL = "[mgbgwwshwind]"
 

$ipParts = $ip.Split('.')
[array]::Reverse($ipParts)
$ipParts = [string]::Join('.', $ipParts)


$blacklists = "dnsbl.httpbl.org", `
	"cbl.abuseat.org", `
	"dnsbl.sorbs.net", `
	"bl.spamcop.net", `
	"zen.spamhaus.org", `
	"b.barracudacentral.org", `
	"bad.psky.me"

foreach ( $blacklist in $blacklists ) {
	if ( $blacklist -contains "dnsbl.httpbl.org" ) {
		
		$lookupAddress = $httpBL + "." + $ipParts + " .dnsbl.httpbl.org."
	}
	else {
		$lookupAddress = $ipParts + ".$blacklist."
	}
	try {
		[System.Net.Dns]::GetHostEntry($lookupAddress) | select-object HostName,AddressList
	}
	catch {

		Write-Host "No blacklisting for $ip found in $blacklist"
	}
}
