const getGlobalThis = () => globalThis;

getGlobalThis.getPolyfill = () => globalThis;
getGlobalThis.implementation = globalThis;
getGlobalThis.shim = () => globalThis;

export default getGlobalThis;
