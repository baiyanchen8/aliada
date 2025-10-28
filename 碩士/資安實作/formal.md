這份筆記是根據兩份文件（《Formal\_Security\_Proof\_Concept.pdf》和《image.pdf》的摘錄）整理而成，內容涵蓋密碼學基礎、可證實安全性（Provable Security）的方法論、計算複雜性假設，以及安全性概念的定義。

This note is compiled based on the two sources ("Formal\_Security\_Proof\_Concept.pdf" excerpts and "image.pdf" excerpts). It covers the basics of cryptography, the methodology of provable security, computational complexity assumptions, and definitions of security notions.

***

# 整合筆記：可證實安全性概念 (Integrated Notes: Formal Security Proof Concept)

## 一、密碼學簡介與經典目標 (I. Introduction to Cryptography and Classic Goals)

### 1. 密碼學的定義 (Definition of Cryptography)

密碼學是一門研究**系統（方案、協議）**的學科，這些系統即使在**主動干擾者（active disrupter）**存在的情況下，仍能保持其**功能性（目標）**。

> Cryptography is the discipline that studies **systems (schemes, protocols)** that preserve their **functionality (their goal)** even under the presence of an **active disrupter**.

### 2. 經典問題/目標 (Classic Problems/Goals)

密碼學的經典目標包括資訊安全的三大原則（機密性、完整性、可用性）加上認證和不可否認性：

| 目標 (Goal) | 定義 (Definition) | 說明 (Explanation) |
| :--- | :--- | :--- |
| **機密性/保密性 (Secrecy/Confidentiality)** | 訊息不被其他人所知。 | 確保未經授權的人無法獲取文件或訊息的任何資訊。例如：儲存文件或發送訊息時。 |
| **完整性 (Integrity)** | 訊息未被更改。 | 確保訊息就像信封未被打開一樣。 |
| **認證性 (Authenticity)** | 訊息來自發送者。 | 分為兩種類型：**互動式**證明身分（例如電話交談）和**非互動式**證明身分（若能說服第三方，則為**簽名**）。非互動式證明通常使用公開金鑰密碼學。 |
| **不可否認性 (Non-repudiation)** | 無法否認。 | 是數位簽章的目標之一。 |

**密碼學簡史 (A Brief History of Cryptography)**:
*   **1918 年以前 (Until 1918)：** 古代史。基於替換和置換的密碼，保密性 = 機制的保密性。
*   **1918-1975 年：** 技術時期。密碼機（如 Enigma），快速、自動化的置換和替換。
*   **1976 年：** 現代密碼學。給定一個方案，使用假設（例如單向函數）來提供安全證據（即證明）。

### 3. 身份匿名性 (Identity Anonymity)

**身份匿名性 (Identity Anonymity)** 定義：一個方案達成身份匿名性，指的是在提交受保護的（匿名）身份證明資訊時，不會暴露真實身份資訊。敵手無法獲得非可忽略的優勢來將受保護的身份連結到兩個真實身份中的任何一個。

身份匿名性安全遊戲 (Anonymous Security Game):
1.  攻擊者選擇兩個身份 $U_0, U_1$。
2.  系統為 $U_b$（$b \in \{0, 1\}$ 隨機選擇）返回一個匿名輔助資訊 $aid$。
3.  攻擊者猜測 $b'$。
4.  **優勢 (Advantage):** $Adv_A^{anon.sys} = \Pr[b' = b] - 1/2$。
5.  如果 $Adv_A^{anon.sys}$ 是**可忽略的 (negligible)**，則該系統被視為匿名安全。

## 二、可證實安全性與歸約證明 (II. Provable Security and Reduction Proofs)

### 1. 對可證實安全性的需求 (The Need for Provable Security)

傳統的安全評估方法是**密碼分析驅動 (Cryptanalysis driven)**：提出解決方案，然後尋找攻擊。這種方法的缺點是：
*   不知道何時停止尋找攻擊。
*   結果不一定可靠（例如：Chor-Rivest 背包方案花了 10 年才被完全破解）。

因此，可證實安全性成為支持新興標準的常見要求。

### 2. 可證實安全性的步驟 (The Recipe for Provable Security)

可證實安全性提供了一個結構化的方法來證明方案的安全性：
1.  定義方案的目標（或敵手的目標）。
2.  定義攻擊模型。
3.  給出協議 (protocol)。
4.  定義複雜性假設（或對原語的假設）。
5.  **提供歸約證明 (Provide a proof by reduction)**。
6.  驗證證明。
7.  解釋證明。

### 3. 歸約證明 (Proof by Reduction)

歸約證明是可證實安全性的核心機制。
*   讓 $P$ 是一個難題 (hard problem)。
*   讓 $A$ 是一個能破解該方案的敵手 (adversary)。
*   **歸約 (Reduction)：** 敵手 $A$ 可以被用來解決難題 $P$。
*   如果發生這種情況，我們稱解決 $P$ **歸約 (reduces)** 為破解該方案。
*   **結論：** 如果 $P$ 是**難以處理的 (untractable)**，那麼該方案就是**不可破解的 (unbreakable)**。

可證實安全性並不是真正證明方案是絕對安全的，而是證明**方案的安全性歸約到潛在假設 (underlying assumption) 的安全性**。因此，它也被稱為**歸約安全性 (Reductionist security)**。

## 三、計算複雜性假設 (III. Computational Complexity Assumptions)

**需要計算假設 (Computational Assumptions)**：
由於密文 $c$ 是由公鑰 $k_e$、訊息 $m$ 和隨機數 $r$ 唯一確定的，因此至少可以進行**窮舉搜索 (exhaustive search)**。因此，**無條件保密性 (Unconditional secrecy)** 是不可能的。我們需要複雜性（算法）假設。

### 1. 單向函數 (One-way Function, OWF)

*   函數 $f: Dom(f) \to Rec(f)$：
    *   計算 $x \to y = f(x)$ 很容易（多項式時間）。
    *   對於隨機 $x$ 而言，計算 $y = f(x) \to x$ 卻很困難（至少是超多項式時間）。
*   敵手 $A$ 的**優勢 (Advantage)** $Adv_{owf}(A)$ 衡量了 $A$ 成功反轉 $f$ 的機率。

### 2. 整數因式分解與 RSA (Integer Factoring and RSA)

*   **因式分解 (Factorization):** $p, q \to n = p \cdot q$ 很容易（二次）。 $n = p \cdot q \to p, q$ 很困難（超多項式）。
*   **RSA 函數:** $f(x) = x^e \mod n$ 很容易。在不知道陷門 $d$ 的情況下，計算 $y \to x$ 很困難。

### 3. 離散對數 (Discrete Logarithm, DLog)

*   在有限循環群 $G = (\langle g \rangle, \times)$ 中：
    *   **指數函數 (Exponentiation):** $x \to y = g^x$ 很容易（立方）。
    *   **離散對數 (DLog):** $y = g^x \to x$ 很困難（超多項式）。

## 四、安全性的解釋與量化 (IV. Interpretation and Quantification of Security)

當進行歸約證明時，我們將敵手 $A$ (在時間 $t$ 內，成功機率 $\epsilon$ 破解方案) 轉換為一個攻擊 $P$ 的算法 (在時間 $t'$ 內，成功機率 $\epsilon'$ 解決 $P$)。

### 1. 三種安全解釋 (Three Interpretations of Security)

1.  **複雜性理論安全性 (Complexity-theory Security):**
    *   歸約 $T$ 是 $t$ 和 $\epsilon$ 的多項式。
    *   結論：不存在多項式時間敵手 (只要參數足夠大)。
2.  **精確安全性 (Exact Security) / 具體安全性 (Concrete Security):**
    *   歸約 $T$ 必須是 $t, \epsilon$ 和其他參數（例如金鑰大小）的**精確成本函數**。
    *   用途：從 $T(t) \le \tau$（解決 $P$ 所需的操作數）可以得出方案安全的最小金鑰大小。
3.  **實用安全性 (Practical Security):** $T$ 較小（線性）。

### 2. 衡量歸約品質 (Measuring the Quality of the Reduction)

*   **緊密度 (Tightness):** 歸約是緊密的，如果 $t' \approx t$ 且 $\epsilon' \approx \epsilon$。
*   **緊密度差距 (Tightness Gap):** $(t'\epsilon)/(t\epsilon')$。我們希望緊密度差距小。

## 五、安全性概念與模型 (V. Security Notions and Models)

### 1. 簽名方案的安全性概念 (Security Notions for Signature Schemes)

*   **攻擊目標：** 存在性偽造 (Existential Forgery, EUF)。敵手在不知道私鑰的情況下，偽造出一個有效的訊息-簽名對 $(m', \sigma')$。
*   **最強攻擊模型：** 選擇訊息攻擊 (Chosen-Message Attack, CMA)。敵手可以選擇訊息，並獲得其訊息/簽名對。
*   **安全性概念：** 在選擇訊息攻擊下的存在性不可偽造性 (Existential Unforgeability under Chosen-Message Attack, **EUF-CMA**)。

### 2. 加密方案的安全性概念 (Security Notions for Encryption Schemes)

*   **目標：** 不可區分性 (Indistinguishability) 或**語義安全性 (Semantic Security)**。給定密文，敵手無法區分是 $m_0$ 還是 $m_1$ 的加密結果。
*   **語義安全性遊戲 (Semantic Security Game):** 敵手提供 $m_0, m_1$，挑戰者隨機加密 $m_b$ 得到密文 $C$。敵手猜測 $b'$。
*   **最強攻擊模型：** **選擇密文攻擊 (Chosen-Ciphertext Attack, CCA / CCA2)**。敵手可以存取**解密預言機 (decryption oracle)**，（自適應地）解密其選擇的任何密文，除了一個挑戰密文 $c^*$。
*   **安全性概念：** 在選擇密文攻擊下的不可區分性 (**IND-CCA**)。

### 3. 理想化安全模型 (Idealized Security Models)

有時，將密碼學方案中使用的某些工具（原語）視為**理想的 (ideal)** 會很有幫助。
*   **雜湊函數 (Hash function)** $\to$ **隨機預言機 (Random Oracle, RO)**。
    *   RO 被分析為一個完全隨機的函數。每次新的查詢都會得到一個隨機答案。
*   **分組密碼 (Block ciphers)** $\to$ **理想密碼 (Ideal Cipher)**。
*   **有限群 (Finite groups)** $\to$ **通用群 (Generic Group)**。

隨機預言機模型雖然廣泛用於證明實用方案的安全性，但存在爭議，被認為**不完全是證明，只是啟發式 (heuristic)**。

## 六、實例：FDH 數位簽章的精確安全性 (VI. Example: Exact Security of FDH Digital Signatures)

### 1. 全域雜湊簽名方案 (Full-Domain Hash, FDH)

FDH 方案使用陷門單向置換 $f$（例如 RSA 函數）和雜湊函數 $H$。
*   **簽名 (Signature) $\sigma$：** $\sigma \leftarrow f^{-1}(H(m))$。
*   **驗證 (Verification)：** 檢查 $f(\sigma) = H(m)$。

### 2. FDH 的 EUF-CMA 定理 (FDH EUF-CMA Theorem)

在隨機預言機 (RO) 模型下，對於每個攻擊 FDH 的敵手 $A$，存在一個攻擊潛在假設 $f$ (OWF) 的敵手 $B$：
$$Adv_{euf-cma}^{\text{FDH}}(A) \le (q_h + q_s + 1) \cdot Adv_{owf}^f(B)$$
其中 $q_h$ 是雜湊查詢次數， $q_s$ 是簽名查詢次數， $T_f$ 是計算 $f$ 的時間。
敵手 $B$ 運行時間為 $t' = t + (q_h + q_s) \cdot T_f$。

### 3. 遊戲證明法 (Game-based proofs)

精確安全性證明通常使用遊戲證明法（例如 Shoup 2004, Bellare-Rogaway 2004）：
1.  定義一系列的遊戲 $G_0, G_1, \dots, G_k$。
2.  $G_0$ 是實際的安全遊戲（例如 EUF-CMA）。
3.  $G_k$ 是潛在假設的遊戲（例如 OWF）。
4.  通過中間遊戲，將 $G_0$ 和 $G_k$ 中定義的優勢事件的機率聯繫起來。

### 4. 結果解釋 (Interpreting the Result)

對於 RSA-FDH：
*   最初的歸約結果 (Bellare-Rogaway 1993, 1996) 顯示，若要抵抗已知最佳攻擊（如 NFS，假設敵手資源上限），RSA 金鑰長度需**至少 4096 位元**。
*   改進後的歸約 (Coron 2000) 顯示，只需**至少 2048 位元**的金鑰即可提供足夠的安全性。

## 七、加密方案的實現 (VII. Implementation of Encryption Schemes)

*   **RSA：** 依賴整數因式分解。本身是**確定性的 (deterministic)**，因此只能達成 OW-CPA，無法達成 IND-CPA 或 IND-CCA。
*   **ElGamal：** 依賴離散對數。達成 IND-CPA，但因為**乘法性 (multiplicativity)**，無法達成 IND-CCA。
*   **f-OAEP (Optimal Asymmetric Encryption Padding)：**
    *   這是一種通用轉換，用於從弱安全方案轉換為強安全方案 (IND-CCA)。
    *   **RSA-OAEP** 在隨機預言機模型中，從 OW-CPA 的變體歸約而來。最初結果表明需要 4096 位元金鑰。
    *   **f-OAEP++** (Jonsson 2002) 使用理想密碼模型代替 OAEP 中的填充，提供了更**緊密 (tight)** 的歸約。
    *   在理想密碼模型下，RSA-OAEP++ 可以在 1024 位元金鑰長度下抵抗合理的攻擊，提供足夠的安全性。

## 八、結論與限制 (VIII. Conclusion and Limitations)

### 1. 可證實安全性的益處 (Benefits)

*   提供了方案沒有缺陷的某種保證。
*   激勵我們以形式化方式闡明（澄清）定義和模型。
*   提供了定義明確的歸約，從中我們可以得出實用意義（精確安全性）。

### 2. 限制與挑戰 (Limits)

*   **證明是相對的：** 相對於計算假設和方案目標的定義。
*   **常在理想模型中完成：** 例如 RO 模型、理想密碼模型等，其意義存在爭議。

---

## English Version (Integrated Notes: Formal Security Proof Concept)

### I. Introduction to Cryptography and Classic Goals

#### 1. Definition of Cryptography

Cryptography is the discipline that studies **systems (schemes, protocols)** that preserve their **functionality (their goal)** even under the presence of an **active disrupter**.

#### 2. Classic Problems/Goals

The classic goals include the principles of information security (Confidentiality, Integrity, Availability) plus Authenticity and Non-repudiation:

| Goal | Definition | Explanation |
| :--- | :--- | :--- |
| **Secrecy / Confidentiality** | Message not known to anybody else. | We want no unauthorized person to learn information about the document or message. Unconditional secrecy is impossible because exhaustive search is possible. |
| **Integrity** | Messages have not been altered. | Analogous to knowing the envelope has not been opened. |
| **Authenticity** | Message comes from sender. | Two types: **Interactive** proof of identity (e.g., phone conversation) or **Non-interactive** proof (a **signature** if it convinces a third party). Non-interactive proof often uses Public-key cryptography. |
| **Non-repudiation** | The inability to deny having performed an action. | A key goal for signature schemes. |

**Cryptography History**: Modern Cryptography began in 1976, focusing on using assumptions (like one-way functions) to show evidence of security (a proof?).

#### 3. Identity Anonymity (From Handwritten Notes)

**Identity Anonymity** Definition: A scheme achieves identity anonymity by submitting protected (anonymous) identity information without exposing the real identity information. The adversary cannot obtain a non-negligible advantage to link the protected ID to one of two real IDs.

Anonymous Security Game: Measures the adversary's advantage ($Adv_A^{anon.sys} = \Pr[b' = b] - 1/2$) in distinguishing which of two identities ($U_0, U_1$) generated the anonymous aid. The system is said to be anonymous secure if $Adv_A^{anon.sys}$ is negligible.

### II. Provable Security and Reduction Proofs

#### 1. The Need for Provable Security

The common approach (Cryptanalysis driven: propose $\to$ attack $\to$ iterate) is problematic because it's hard to know when to stop, and results may not be trustworthy (e.g., Chor-Rivest scheme took 10 years to break). Provable security is now a common requirement for standards.

#### 2. The Recipe for Provable Security

The structured approach of provable security involves seven steps:
1. Define the goal of the scheme (or adversary).
2. Define the attack model.
3. Give a protocol.
4. Define complexity assumptions (or assumptions on the primitive).
5. **Provide a proof by reduction**.
6. Verify the proof.
7. Interpret the proof.

#### 3. Proof by Reduction

A reductionist proof ensures security based on a known hard problem $P$.
*   **The Logic:** If an adversary $A$ can break the scheme (i.e., break the secrecy or integrity), then $A$ can be used to solve the underlying problem $P$.
*   **Conclusion:** If $P$ is intractable, the scheme is unbreakable.
*   Provable security is better described as **Reductionist security**, showing a reduction from the scheme's security to the security of the underlying assumption.

### III. Computational Complexity Assumptions

Computational assumptions are necessary because unconditional secrecy is impossible (due to the feasibility of exhaustive search).

#### 1. One-way Function (OWF)

A function $f$ is a one-way function if computing $x \to y = f(x)$ is easy (polynomial time), but inverting $y \to x$ is difficult for a random $x$ (at least super-polynomial time).

#### 2. Integer Factoring and RSA

*   Multiplication ($p \cdot q \to n$) is easy.
*   Factorization ($n \to p, q$) is hard (super-polynomial).
*   **RSA Function:** $x \to x^e \mod n$ is easy, but inverting $y \to x$ is difficult without the trapdoor $d$.

#### 3. Discrete Logarithm (DLog)

In a finite cyclic group $G$:
*   **Exponentiation:** $x \to y = g^x$ is easy (cubic).
*   **DLog:** Finding $x$ such that $y = g^x$ is difficult (super-polynomial).

### IV. Interpretation and Quantification of Security

#### 1. Types of Security

The interpretation of the reduction matters, relating the adversary's time and success probability ($t, \epsilon$) to the problem-solver's ($t', \epsilon'$).

*   **Complexity-Theory Security:** The reduction time $T$ is polynomial in $t$ and $\epsilon$. Result: Guarantees no polynomial-time adversary exists (if parameters are large enough).
*   **Exact Security:** Provides the **exact cost** $T$ as a function of $t, \epsilon$, and key sizes. This is useful for deriving bounds on **minimal key sizes** necessary for security.
*   **Practical Security:** Requires $T$ to be small (linear).

#### 2. Measuring Reduction Quality

A reduction is **tight** if $t' \approx t$ and $\epsilon' \approx \epsilon$. The tightness gap is measured as $(t'\epsilon)/(t\epsilon')$. Tight reductions are desirable.

### V. Security Notions and Models

#### 1. Signature Schemes

*   **Goal:** **Existential Forgery (EUF)**.
*   **Strongest Attack Model:** **Chosen-Message Attack (CMA)**, where the adversary can choose messages and receive valid message/signature pairs from a Signing Oracle.
*   **Security Notion:** **EUF-CMA**.

#### 2. Encryption Schemes

*   **Goal:** **Indistinguishability (Semantic Security)**. The adversary cannot tell apart two ciphertexts encrypting two different, chosen messages.
*   **Semantic Security Game:** Attacker submits $m_0, m_1$. Challenger returns $C = E(m_b)$ for random $b$. Attacker guesses $b'$. The scheme is semantically secure if the advantage $Adv_{E}^{(E,D)}(A) = \Pr[b'=b] - 1/2$ is negligible.
*   **Strongest Attack Model:** **Chosen-Ciphertext Attack (CCA / CCA2)**, where the adversary has adaptive access to a Decryption Oracle (except for the challenge ciphertext $c^*$).
*   **Security Notion:** **IND-CCA**.

#### 3. Idealized Security Models

These models consider tools like hash functions or block ciphers to be ideal primitives.
*   **Hash function** $\to$ **Random Oracle (RO)**. The RO is analyzed as a perfectly random function.
*   **Block ciphers** $\to$ **Ideal Cipher**.
*   The RO model is arguably the most used for practical schemes, but it is somewhat controversial, as it is seen as a heuristic rather than a true proof.

### VI. Examples: FDH and RSA-OAEP

#### 1. Full-Domain Hash (FDH) Signatures

FDH uses a trapdoor one-way permutation $f$ (like RSA) and a hash function $H$ (modeled as RO). The signature is $\sigma \leftarrow f^{-1}(H(m))$.

*   **Exact Security Result (EUF-CMA in RO model):** The scheme's advantage $Adv_{FDH}(A)$ is bounded by $(q_h + q_s + 1)$ times the advantage of inverting the one-way function $f$ ($Adv_{owf}^f(B)$).
*   **Game-Based Proofs:** This security is shown by defining a sequence of games ($G_0$ to $G_5$) that gradually transform the EUF-CMA game ($G_0$) into the OWF problem ($G_5$), relating the probabilities of success in each step.
*   **Interpretation:** Using the tightness results, RSA-FDH is typically deemed secure for keys of **at least 2048 bits** (based on Coron's improved reduction).

#### 2. Achieving IND-CCA with RSA-OAEP

Since native RSA is deterministic and only achieves OW-CPA, generic conversions are needed to achieve the strong IND-CCA security.

*   **RSA-OAEP** is a popular construction. A good reduction in the RO model was given, but initial analysis suggested large keys (4096 bits) were needed to compete with factoring difficulty estimates.
*   **f-OAEP++** (Jonsson 2002) uses a tighter reduction (in the Ideal Cipher Model) that is essentially linear. This analysis shows that RSA-OAEP++ provides sufficient security even with **1024-bit keys** against feasible attacks.

### VII. Concluding Remarks

Provable security, while not yielding absolute proofs (since proofs are relative to computational assumptions and done often in idealized models), is beneficial because it provides a guarantee against flaws, motivates formal definitions, and allows the distillation of practical implications (exact security).