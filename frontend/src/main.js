import { wrap } from "svelte-spa-router/wrap";
import Router from "svelte-spa-router";
import App from "./App.svelte";
import { Button } from 'flowbite-svelte';

const app = new App({
  target: document.body
});

export default app;
