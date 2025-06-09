inpage.js:1 MetaMask - RPC Error: execution reverted 
{code: 3, message: 'execution reverted', data: '0xfb8f41b2000000000000000000000000d49afbad123a30cf…000000000000000000000000000000000011c37937e080000', stack: '{\n  "code": 3,\n  "message": "execution reverted",\n…fbeogaeaoehlefnkodbefgpgknn/common-2.js:1:1391130'}
code
: 
3
data
: 
"0xfb8f41b2000000000000000000000000d49afbad123a30cfa9fa7c9b4e685ecc95faa5710000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011c37937e080000"
message
: 
"execution reverted"
stack
: 
"{\n  \"code\": 3,\n  \"message\": \"execution reverted\",\n  \"data\": \"0xfb8f41b2000000000000000000000000d49afbad123a30cfa9fa7c9b4e685ecc95faa5710000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011c37937e080000\",\n  \"stack\": \"Error: execution reverted\\n    at new i (chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/common-4.js:1:81689)\\n    at d.request (chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/common-1.js:3:17766)\\n    at async chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/background-0.js:1:424918\\n    at async chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/common-2.js:1:1391130\"\n}\n  at new i (chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/common-4.js:1:81689)\n  at d.request (chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/common-1.js:3:17766)\n  at async chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/background-0.js:1:424918\n  at async chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/common-2.js:1:1391130"
[[Prototype]]
: 
Object
index.js??clonedRule…up=true&lang=js:124 Contract call failed: Error: execution reverted (unknown custom error) (action="estimateGas", data="0xfb8f41b2000000000000000000000000d49afbad123a30cfa9fa7c9b4e685ecc95faa5710000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011c37937e080000", reason=null, transaction={ "data": "0x25a7290900000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000007a3b00000000000000000000000000000000000000000000000000000000000095650000000000000000000000000000000000000000000000006de97e09bd1800000000000000000000000000000000000000000000000000000000000068371410000000000000000000000000003034e029d434e38a4aa7f50d6c7cfa26469d3a000000000000000000000000000000000000000000000000011c37937e080000000000000000000000000000000000000000000000000000000000000000014000000000000000000000000000000000000000000000000000000000000000055445534c4100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000419f9a563bdf3e8160a83294d1b93783933f286f94787969a7f24ee6ccc03d97ef165e934b2dc08893472b91e4cb60e32a99ff8b4c8ae9633b0572c599369bb7a11c00000000000000000000000000000000000000000000000000000000000000", "from": "0x003034e029d434e38a4AA7f50d6C7CFa26469d3a", "to": "0xd49AFbad123a30CFA9fA7c9B4E685eCc95faA571" }, invocation=null, revert=null, code=CALL_EXCEPTION, version=6.14.0)
    at makeError (errors.js:144:15)
    at getBuiltinCallException (abi-coder.js:122:68)
    at AbiCoder.getBuiltinCallException (abi-coder.js:197:12)
    at BrowserProvider.getRpcError (provider-jsonrpc.js:714:70)
    at BrowserProvider.getRpcError (provider-browser.js:114:18)
    at eval (provider-jsonrpc.js:976:27)
confirmContract	@	index.js??clonedRule…up=true&lang=js:124
await in confirmContract		
callWithErrorHandling	@	runtime-core.esm-bundler.js:384
callWithAsyncErrorHandling	@	runtime-core.esm-bundler.js:391
invoker	@	runtime-dom.esm-bundler.js:941