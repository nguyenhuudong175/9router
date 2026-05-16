# System Execution Sequence Diagram: 9router

```mermaid
sequenceDiagram
    participant DevTool as Developer Tool (Cursor, Cline, Codex, etc.)
    participant Proxy as 9Router Proxy Server
    participant Sub as Subscription Provider (Claude, Codex, Gemini)
    participant Cheap as Cheap Provider (GLM, MiniMax, Kimi)
    participant Free as Free Provider (iFlow, Qwen, Kiro)

    DevTool->>Proxy: Send AI API Request (OpenAI-compatible)
    Proxy->>Proxy: Check quota for Subscription Providers
    alt Subscription quota available
        Proxy->>Sub: Forward request
        Sub-->>Proxy: Response (compressed)
        Proxy->>Proxy: Apply token compression (RTK + Caveman)
    else No subscription or quota exhausted
        Proxy->>Proxy: Check quota for Cheap Providers
        alt Cheap provider quota available
            Proxy->>Cheap: Forward request
            Cheap-->>Proxy: Response (compressed)
            Proxy->>Proxy: Apply token compression
        else No cheap quota or error
            Proxy->>Proxy: Route to Free Providers
            Proxy->>Free: Forward request
            Free-->>Proxy: Response (compressed)
            Proxy->>Proxy: Apply token compression
        end
    end
    Proxy->>DevTool: Return unified response
```

This diagram traces the main system flow: developer tools send requests to 9router, which routes the call based on quota/cost, applies token optimization, and relays the result back in the original tool’s expected format.