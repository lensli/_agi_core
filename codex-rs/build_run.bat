@REM cargo fetch
cargo build
cargo run --bin codex
@REM > - 主 CLI 可执行文件叫 codex.exe，由 codex-cli（cli/Cargo.toml）这个包生成；构建后会落在 target/<target三元组>/release/codex.exe，本机默认目标就是 target/release/codex.exe。                                                         
@REM   - 发布流程里还会同时打出配套的 codex-responses-api-proxy.exe（同目录下）。在 ../.github/workflows/rust-release.yml 可以看到 Windows 平台最终就是这两个二进制被收集、压缩后上传发布。                                                 
@REM   - 本地打包最快的方式是用稳定版 Rust：cargo build --release --bin codex --bin codex-responses-api-proxy；如果只需要 CLI，可只保留 --bin codex。                                                                                       
@REM   - 需要跨平台包时先 rustup target add <triple>，然后例如 cargo build --release --target x86_64-pc-windows-msvc --bin codex --bin codex-responses-api-proxy；生成的二进制会在 target/x86_64-pc-windows-msvc/release/。                 
@REM   - 若想复刻 CI 的发布产物，可在构建后把两个 .exe 复制到某个 dist/<target> 目录，再按需生成 .tar.gz / .zip / .zst 压缩包（CI 里使用 zstd 和 7z 完成这一步）。  
