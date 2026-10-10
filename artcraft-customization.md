# Using Your Own Provider Keys and Local Models with ArtCraft

Oct 10, 2026 · @Avkash Chauhan

## Summary

You can generate images in ArtCraft with your own **FAL API key** today, including Nano Banana 2, Nano Banana Pro and FLUX. Text-only prompts on this route need no ArtCraft credits. There is no Google/Gemini key option and no local-model provider; both need code changes in a self-built app.

Findings come from reading [storytold/artcraft](https://github.com/storytold/artcraft) at commit `910bfe4` (9 Oct 2026).

| What you want | Works today? | How |
| --- | --- | --- |
| Your own FAL key for images | Yes | Write the key to `~/Artcraft/credentials/fal.api_key.txt`, then pick **Fal** as the provider |
| Your own Google Gemini (Nano Banana) key | No | Add a new provider in a self-built app (see Local models and new providers) |
| Local models (ComfyUI, Ollama-style servers, etc.) | No | Add a new provider in a self-built app |
| Midjourney, Grok, Sora, World Labs | Yes | Sign in with your own account for that service |
| Your own key for video | No | Video goes through ArtCraft credits, Grok or Sora only |
| FAL key through this ArtCraft MCP | No | The MCP is subscription-only |

Recommended path: use the FAL key file now. If you need Google keys or local models, add a provider in your own build of the app.

## How provider routing works

`generate_image_command` reads the request's `provider` and defaults to ArtCraft. ArtCraft and Midjourney have their own handlers. Every other provider goes to the router, which loads your credential from `~/Artcraft/credentials/` and handles only FAL. Other providers return "does not have a mapped credential key yet".

&#91;embedded content: image provider routing · 3 branches\]

Key files, under `crates/desktop/artcraft/src/core/`:

- `commands/generate/generate_image/generate_image_command.rs`: chooses the provider
- `commands/generate/generate_image/providers/artcraft_router/handle_router.rs`: maps each provider to its credential key
- `commands/generate/generate_image/providers/artcraft_router/handle_api_providers.rs`: the FAL handler
- `providers/credentials/provider_credential_key.rs`: credential file names
- `commands/generate/generate_video/generate_video_command.rs`: video routing (Grok, Sora, otherwise ArtCraft)

## Use your own FAL key (stock or self-built app)

The app has a working backend for FAL keys but no settings screen to enter one. You write the key file yourself. The **Set up Fal** button in the provider setup modal does nothing; its handler is marked `// TODO: None yet.`.

1. Create a key at [fal.ai](https://fal.ai) and add billing there. FAL charges you per image.
2. Quit ArtCraft.
3. Save the key where the app's credential cache reads it:

   ```bash
   mkdir -p ~/Artcraft/credentials
   read -rs FAL_KEY && printf '%s' "$FAL_KEY" > ~/Artcraft/credentials/fal.api_key.txt
   chmod 600 ~/Artcraft/credentials/fal.api_key.txt
   ```

   `read -rs` keeps the key out of your shell history. The app trims whitespace when it loads the file.
4. Start ArtCraft and choose a model that lists FAL as a provider: Nano Banana 2, Nano Banana Pro, FLUX.1 \[dev\] or FLUX.1 \[schnell\].
5. In the provider picker next to the model, choose **Fal** instead of **ArtCraft**, then generate.

If you see "You need to set a FAL api key", the file is missing or in the wrong place. The new file name is `fal.api_key.txt` (with a dot). The older `fal_api_key.txt` is only read by legacy 3D, background-removal and Kling commands.

In a self-built app you can skip the file: the registered Tauri command `provider_set_api_key_command` takes `{ provider_credential: "fal_api_key", api_key }` and writes the same file. Exposing it in Settings → Accounts is a small frontend change.

## Which models run on which route

The UI offers FAL for four image models, but the backend maps 22 model IDs to FAL. A self-built app can expose the rest by adding `GenerationProvider.Fal` to each model's `providers` in `frontend/libs/model-list/src/lib/lists/ImageModels.ts`.

| Route | Your credential | Models in the UI today | Also mapped in the backend | Code |
| --- | --- | --- | --- | --- |
| FAL (images) | FAL API key | Nano Banana 2, Nano Banana Pro, FLUX.1 \[dev\], FLUX.1 \[schnell\] | Nano Banana, FLUX 1.1 Pro / Ultra, GPT Image 1 / 1.5 / 2 / 2.5, Seedream 4 / 4.5 / 5 Lite, Midjourney 7 / 8, Qwen Edit, Flux 2 LoRA | `tauri_image_model_to_router_model` |
| Midjourney | Midjourney login | Midjourney | — | `handle_midjourney` |
| Grok | Grok login | Grok Video | — | `handle_grok_video` |
| Sora | Sora login | Sora 2 | — | `handle_sora_sora2` |
| FAL (legacy tools) | `fal_api_key.txt` | Background removal, Hunyuan image-to-3D, Kling image-to-video | — | `frontend/libs/tauri-api/src/lib/fal/` |
| ArtCraft | ArtCraft credits | All models on the server's model list | — | `handle_artcraft` |

Gaps:

- Not on any own-key route: Seedream 5.0 Pro, Seedream 5.0 Pro Ultra, Recraft 3, FLUX Kontext Max.
- New video generation sends every model except Grok and Sora through ArtCraft credits. The request's `provider` field is ignored for other video models.
- `ReplicateApiKey`, plus Higgsfield and Runway logins, exist as credential keys but no generation path uses them yet.

## Local models and new providers (self-built app)

ArtCraft has no local-inference provider: every generation path calls a remote API. ComfyUI or other local servers, and a direct Google Gemini key, both need a new provider in your own build. FAL is a working example to copy.

Changes, in the order a request flows:

1. **Provider enum.** Add a variant, e.g. `Local` or `Google`, to `GenerationProvider` in `crates/schema/public/enums/src/common/generation_provider.rs`. Keep the string to 16 characters or fewer, and update `to_str` / `from_str` and the TypeScript `GenerationProvider` enum.
2. **Credential key.** Add `GoogleApiKey` (API key) or `LocalEndpoint` (a URL stored as an API-key-type file) to `ProviderCredentialKey`, with a file name in `get_filename()`, e.g. `google.api_key.txt`.
3. **Router mapping.** In `handle_router.rs`, map the new provider to its key in `map_provider_to_credential_key` and to a missing-credentials error.
4. **Handler.** In `handle_api_providers.rs`, add a branch beside `GenerationProvider::Fal` that calls your API. For Gemini, call `generateContent` on a `gemini-*-image` model. For a local server, POST to your ComfyUI or other endpoint.
5. **Results.** FAL jobs finish on `third_party_task_polling_thread/handlers/fal`. Add a handler for an async API, or save the image straight to the task database if your call is synchronous.
6. **Router crate (optional).** For router features like option-mismatch handling, add `RouterProvider::Google` / `Local` and a client in `crates/api_clients/artcraft/artcraft_router`, next to `RouterFalClient`.
7. **UI.** Add the provider to each model's `providers` in `ImageModels.ts`, and add a key or endpoint field to Settings → Accounts that calls `provider_set_api_key_command`.

Build and run with `./script/artcraft/unix_dev.sh`, as in the repo's [dev setup guide](https://github.com/storytold/artcraft/blob/main/_docs/dev_setup.md). Check that the license allows your use before you distribute a modified build.

## Caveats

- **ArtCraft sign-in is optional for text prompts.** On the FAL route, the app tries to save the prompt to your ArtCraft account. If you're signed out, it logs a warning and continues.
- **Reference images still go through ArtCraft.** Uploaded references are ArtCraft media tokens. The FAL handler turns them into ArtCraft CDN URLs, so image editing on FAL needs an ArtCraft account to upload to.
- **The ArtCraft MCP can't use your key.** `artcraft-mcp/server.py` calls only the subscription API, so it returns HTTP 402 with no credits. Using a FAL key from Claude Code or Hermes would need a new tool that reads `fal.api_key.txt` and calls FAL directly.
- **Keys are stored as plain text.** Keep `~/Artcraft/credentials/` at mode 600. Never commit it, and never paste a key into chat or a prompt.
- **This reflects one commit.** The provider code is changing; the README lists Google, Kling, Runway and Luma as planned integrations. Recheck these paths after you update the app.
