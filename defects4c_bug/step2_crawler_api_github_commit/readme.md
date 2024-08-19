This folder is intend to crawler the cotnent by giuven a commit url from api.github.com 


At begin, data from gharchive.com (or BigQuery) only includes event types and commit URLs. As a result, the SQL query result yields only the commit URLs. In Step 2, by indexing these commit URLs to ask content from api.github.com, we can retrieve meta-information such as bug commits and changing content. This step allows us to determine whether the changes are confined to a single source file and whether they occur within a single function. Therefore step 2 is crucial for subsequent steps, as it provides the necessary content to build a corpus for further analysis.


Here, we provide a JSON result retrieved from api.github.com to illustrate the mechanism.

<details>
  <summary>Click me to see the json example from api.github.com, from url: https://www.github.com/llvm/llvm-project/commit/54b25c249a781c72b84bfbaf09d9f1fffc448db8 </summary>
  
```json

{
  "sha": "54b25c249a781c72b84bfbaf09d9f1fffc448db8",
  "node_id": "MDY6Q29tbWl0NzU4MjE0MzI6NTRiMjVjMjQ5YTc4MWM3MmI4NGJmYmFmMDlkOWYxZmZmYzQ0OGRiOA==",
  "commit": {
    "author": {
      "name": "git apple-llvm automerger",
      "email": "am@git-apple-llvm",
      "date": "2020-10-21T18:32:10Z"
    },
    "committer": {
      "name": "git apple-llvm automerger",
      "email": "am@git-apple-llvm",
      "date": "2020-10-20T20:45:39Z"
    },
    "message": "Merge commit 'c5acd3490b79' from llvm.org/master into apple/main",
    "tree": {
      "sha": "c3ee7d7d928ef17da4f693cf7c9a7d70677f5306",
      "url": "https://api.github.com/repos/llvm/llvm-project/git/trees/c3ee7d7d928ef17da4f693cf7c9a7d70677f5306"
    },
    "url": "https://api.github.com/repos/llvm/llvm-project/git/commits/54b25c249a781c72b84bfbaf09d9f1fffc448db8",
    "comment_count": 0,
    "verification": {
      "verified": false,
      "reason": "unsigned",
      "signature": null,
      "payload": null
    }
  },
  "url": "https://api.github.com/repos/llvm/llvm-project/commits/54b25c249a781c72b84bfbaf09d9f1fffc448db8",
  "html_url": "https://github.com/llvm/llvm-project/commit/54b25c249a781c72b84bfbaf09d9f1fffc448db8",
  "comments_url": "https://api.github.com/repos/llvm/llvm-project/commits/54b25c249a781c72b84bfbaf09d9f1fffc448db8/comments",
  "author": null,
  "committer": null,
  "parents": [
    {
      "sha": "130a0a06364facbbb401fbe2c4cf92482188f270",
      "url": "https://api.github.com/repos/llvm/llvm-project/commits/130a0a06364facbbb401fbe2c4cf92482188f270",
      "html_url": "https://github.com/llvm/llvm-project/commit/130a0a06364facbbb401fbe2c4cf92482188f270"
    },
    {
      "sha": "c5acd3490b79703426931f7b88b544fe7c6e1ef2",
      "url": "https://api.github.com/repos/llvm/llvm-project/commits/c5acd3490b79703426931f7b88b544fe7c6e1ef2",
      "html_url": "https://github.com/llvm/llvm-project/commit/c5acd3490b79703426931f7b88b544fe7c6e1ef2"
    }
  ],
  "stats": {
    "total": 10,
    "additions": 8,
    "deletions": 2
  },
  "files": [
    {
      "sha": "68ae25e9cc2024f95eb1cd3a05ba62632bb9911a",
      "filename": "clang/lib/Driver/SanitizerArgs.cpp",
      "status": "modified",
      "additions": 1,
      "deletions": 2,
      "changes": 3,
      "blob_url": "https://github.com/llvm/llvm-project/blob/54b25c249a781c72b84bfbaf09d9f1fffc448db8/clang%2Flib%2FDriver%2FSanitizerArgs.cpp",
      "raw_url": "https://github.com/llvm/llvm-project/raw/54b25c249a781c72b84bfbaf09d9f1fffc448db8/clang%2Flib%2FDriver%2FSanitizerArgs.cpp",
      "contents_url": "https://api.github.com/repos/llvm/llvm-project/contents/clang%2Flib%2FDriver%2FSanitizerArgs.cpp?ref=54b25c249a781c72b84bfbaf09d9f1fffc448db8",
      "patch": "@@ -60,8 +60,7 @@ static const SanitizerMask AlwaysRecoverable =\n     SanitizerKind::KernelAddress | SanitizerKind::KernelHWAddress;\n static const SanitizerMask NeedsLTO = SanitizerKind::CFI;\n static const SanitizerMask TrappingSupported =\n-    (SanitizerKind::Undefined & ~SanitizerKind::Vptr) |\n-    SanitizerKind::UnsignedIntegerOverflow | SanitizerKind::ImplicitConversion |\n+    (SanitizerKind::Undefined & ~SanitizerKind::Vptr) | SanitizerKind::Integer |\n     SanitizerKind::Nullability | SanitizerKind::LocalBounds |\n     SanitizerKind::CFI | SanitizerKind::FloatDivideByZero |\n     SanitizerKind::ObjCCast;"
    },
    {
      "sha": "800b7f68d3c0999d0d651b33631ddd063f756abb",
      "filename": "clang/test/Driver/fsanitize.c",
      "status": "modified",
      "additions": 7,
      "deletions": 0,
      "changes": 7,
      "blob_url": "https://github.com/llvm/llvm-project/blob/54b25c249a781c72b84bfbaf09d9f1fffc448db8/clang%2Ftest%2FDriver%2Ffsanitize.c",
      "raw_url": "https://github.com/llvm/llvm-project/raw/54b25c249a781c72b84bfbaf09d9f1fffc448db8/clang%2Ftest%2FDriver%2Ffsanitize.c",
      "contents_url": "https://api.github.com/repos/llvm/llvm-project/contents/clang%2Ftest%2FDriver%2Ffsanitize.c?ref=54b25c249a781c72b84bfbaf09d9f1fffc448db8",
      "patch": "@@ -786,6 +786,13 @@\n // CHECK-UBSAN-MINIMAL: \"-fsanitize={{((signed-integer-overflow|integer-divide-by-zero|shift-base|shift-exponent|unreachable|return|vla-bound|alignment|null|pointer-overflow|float-cast-overflow|array-bounds|enum|bool|builtin|returns-nonnull-attribute|nonnull-attribute),?){17}\"}}\n // CHECK-UBSAN-MINIMAL: \"-fsanitize-minimal-runtime\"\n \n+// RUN: %clang -target x86_64-linux-gnu -fsanitize=integer -fsanitize-trap=integer %s -### 2>&1 | FileCheck %s --check-prefix=CHECK-INTSAN-TRAP\n+// CHECK-INTSAN-TRAP: \"-fsanitize-trap=integer-divide-by-zero,shift-base,shift-exponent,signed-integer-overflow,unsigned-integer-overflow,unsigned-shift-base,implicit-unsigned-integer-truncation,implicit-signed-integer-truncation,implicit-integer-sign-change\"\n+\n+// RUN: %clang -target x86_64-linux-gnu -fsanitize=integer -fsanitize-minimal-runtime %s -### 2>&1 | FileCheck %s --check-prefix=CHECK-INTSAN-MINIMAL\n+// CHECK-INTSAN-MINIMAL: \"-fsanitize=integer-divide-by-zero,shift-base,shift-exponent,signed-integer-overflow,unsigned-integer-overflow,unsigned-shift-base,implicit-unsigned-integer-truncation,implicit-signed-integer-truncation,implicit-integer-sign-change\"\n+// CHECK-INTSAN-MINIMAL: \"-fsanitize-minimal-runtime\"\n+\n // RUN: %clang -target aarch64-linux-android -march=armv8-a+memtag -fsanitize=memtag -fsanitize-minimal-runtime %s -### 2>&1 | FileCheck %s --check-prefix=CHECK-MEMTAG-MINIMAL\n // CHECK-MEMTAG-MINIMAL: \"-fsanitize=memtag\"\n // CHECK-MEMTAG-MINIMAL: \"-fsanitize-minimal-runtime\""
    }
  ]
}
```

</details>




The scripts are designed to interact with a Redis cluster in a consumer-producer mode. GitHub strictly constrait the rate limits on its API, so our crawlers use GitHub tokens from co-authors' contributions to manage load balancing and alleviate rate limit constraints. For more details, please refer to the code.
