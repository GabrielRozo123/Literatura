# Coluna de Bolhas: resultados CFD 2D axissimétrico

**Projeto:** Seminário de Cinética, reator de coluna de bolhas
**Autor:** Gabriel Rozo | FEQ/UNICAMP
**Status:** ✅ 4 rodadas concluídas a U_G = 2 cm/s
**Dados e scripts:** `Programacao/coluna_bolhas/resultados_cfd_2D/` e `figura_resumo_rodadas.py`

---

## 1. Configuração comum

| Parâmetro | Valor |
|-----------|-------|
| Geometria | Coluna D = 0,15 m, H = 1,2 m, líquido parado H0 = 0,90 m (2D axissimétrico, eixo = X) |
| Malha | 2D, base 2,5 mm (~14 mil células) |
| Física | Implicit Unsteady, EMP, **Mixture Turbulence** (k-ε), Gravity, ρ_ref = 1,18 kg/m³ |
| Fases | Água: 997 kg/m³, 8,9e-4 Pa·s · Ar: 1,18 kg/m³, 1,8e-5 Pa·s |
| Interação | Arrasto de Tomiyama, massa virtual, dispersão turbulenta, σ = 0,072 N/m |
| Aspersor | Velocity Inlet **diluído**: média α_ar = 0,1 a 0,2 m/s, com água em repouso, ou seja U_G = 0,02 m/s |
| Saída | Pressure Outlet no topo (espaço de ar), backflow de ar puro |
| Tempo | Δt de 0,001 a 0,005 s; média temporal a partir de 10–20 s |

## 2. Rodadas

| # | Mudança | εG global | V_L no eixo | V_L máx / mín [m/s] | Inversão r/R | Leitura |
|---|---------|-----------|-------------|---------------------|--------------|---------|
| 1 | d = **1 mm** (valor padrão esquecido), aspersor uniforme | **0,172** | −0,079 | +0,03 / −0,08 | 0,60 | bolhas lentas (U = 0,116 m/s = U∞ de 1 mm pelo arrasto de Tomiyama) |
| 2 | d = **5 mm**, uniforme | **0,0865** | 0,001 | ≈ 0 | — | coluna "homogênea ideal": α plano, sem circulação |
| 3 | d = 5 mm, **aspersor parabólico** (α = 0,2[1−(r/R)²], mesma vazão) | **0,0884** | +0,028 | +0,03 / −0,02 | 0,60 | a circulação aparece no sentido certo, mas fraca: a dispersão turbulenta achata α até z = 0,6 m |
| 4 | idem 3 + **lift C_L = −0,05** (como no tutorial Hibiki) | **0,0856 ± 0,0008** | +0,056 | +0,09 / −0,09 | **0,70** | gás mantido no centro e circulação ~3× mais forte; inversão no valor clássico |

**Estacionariedade da rodada 4:** as médias da 1ª e da 2ª metade da janela de 12 a 30 s diferem em +1,8 % (critério < 2 %). O holdup oscila com período da ordem de uma volta de circulação (~10 s).

## 3. Comparação com a literatura (U_G = 2 cm/s, D = 0,15 m)

| Referência | εG | Desvio do CFD (rodada 4) |
|------------|-----|--------------------------|
| Akita & Yoshida (1973) | 0,055 | +56 % |
| Hikita et al. (1980) | 0,062 | +38 % |
| Média das 3 correlações | 0,074 | +16 % |
| **CFD, rodada 4** | **0,086** | — |
| Homogêneo ideal, d = 5 mm (drift-flux) | 0,096 | −11 % |
| Reilly et al. (1986) | 0,105 | −18 % |

O CFD fica **dentro da faixa das correlações** (0,055–0,105), mais perto do limite homogêneo ideal.

## 3b. Validação com dados experimentais recentes

Figura: `Programacao/coluna_bolhas/resultados/fig_cfd_vs_literatura.png`

| Experimento | Coluna / aspersor | εG a 2 cm/s | CFD (0,086), desvio |
|-------------|-------------------|-------------|---------------------|
| **Mudde et al. (2009)**, via Draw & Rzehak (2024), Tab. 2 | **D = 0,15 m** (igual à nossa), 599 agulhas → distribuição **uniforme** | **0,089** (interpolado entre 0,076 a 1,7 cm/s e 0,11 a 2,5 cm/s) | **−3 %** |
| **Besagni & Inzoli (2016)**, Fig. 14 | D = 0,24 m, *spider* com furos de 1–3,5 mm → **má distribuição** | **0,069** (digit.) / 0,061 (Eq. 31 dos autores) | +25 % / +40 % |

**Leitura física (o resultado mais importante do trabalho):**

- **Experimentalmente,** com a mesma vazão de gás e colunas de porte parecido, o tipo de aspersor muda εG em ~30 % (0,069 → 0,089).
  - As agulhas de Mudde dão um regime homogêneo "verdadeiro": a curva εG × U_G segue o limite homogêneo ideal até ~4 cm/s, com circulação de líquido quase nula (0,004–0,02 m/s no eixo).
  - O aspersor *spider* de Besagni gera circulação e segue as correlações clássicas.
- **O CFD com distribuição uniforme reproduz o caso das agulhas com −3 %.** Draw & Rzehak (2024) obtiveram o mesmo comportamento com o modelo *baseline* do HZDR: εG ≈ 0,067 para J_G = 1,5 cm/s (exp. 0,061) e velocidade do líquido no eixo de 0,008–0,03 m/s para bolhas de 3,5–5 mm (Tab. 6).
- **Confirmações independentes das nossas escolhas de modelo:**
  - a entrada diluída com o gás a 0,2 m/s é **idêntica** à usada por Draw & Rzehak;
  - o diâmetro de 5 mm está dentro da faixa medida (3,5–5 mm em Mudde; 2,5–4 mm em Besagni);
  - a pouca circulação no caso uniforme é física, e não um defeito do 2D.
- **O caso do aspersor *spider* (circulação forte) é o que o 2D axissimétrico não captura bem.** Ele exigiria o 3D ou um aspersor não uniforme mais realista.
- **Sensibilidade ao diâmetro (Draw & Rzehak, Tab. 6):** de 5 para 5,75 mm, o coeficiente de lift troca de sinal e εG cai 20 %. Isso é coerente com o nosso slide de sensibilidade ao diâmetro de bolha.

## 4. Conclusões para o seminário

1. **O diâmetro de bolha controla εG.** De 1 mm para 5 mm, εG cai pela metade (0,172 → 0,086). Num modelo monodisperso, o diâmetro é um *dado de entrada*. Isso motiva modelos de balanço populacional (S-Gamma).
2. **O aspersor e as forças entre as fases controlam a circulação.** A mesma vazão de gás produz desde nenhuma circulação (rodada 2) até ~0,09 m/s com inversão em r/R = 0,7 (rodada 4). A circulação é a origem física do D_L do modelo de dispersão axial, que entra na equação de projeto (Pe ≈ 0,3, ou seja, a fase líquida se comporta quase como um CSTR).
3. **εG global é pouco sensível à circulação no 2D** (0,086–0,088 nas rodadas 2 a 4). O CFD com aspersor uniforme concorda com o experimento de aspersor uniforme (Mudde, −3 %). Akita & Yoshida e Hikita ficam abaixo porque representam aspersores grosseiros com circulação (Besagni: 0,069). Ver seção 3b.
4. **Limitação do 2D axissimétrico.** A circulação no eixo (0,06–0,09 m/s) ficou cerca de 3× abaixo de Riquarts (0,25 m/s). A pluma oscilante, que alimenta a circulação real, só existe em 3D.
5. **Lição numérica.** A primeira tentativa, com ar puro (α = 1) no fundo inteiro, formou uma camada de gás instável e divergiu. A condição de contorno tem de respeitar a física do aspersor.

## 5. Impacto nas equações de projeto (cinética + transferência de massa)

Script: `Programacao/coluna_bolhas/cfd_para_projeto.py`, figura `resultados/fig_cfd_para_projeto.png`. Exemplo: reação de pseudo-1ª ordem no líquido, k1 = 0,01 1/s (Ha = 0,013, regime lento), u_L = 5 mm/s.

| Caso | εG | a [1/m] | kLa [1/s] | k1εL/kLa | k_ef [1/s] | D_L [m²/s] | Pe | X |
|------|-----|---------|-----------|----------|------------|------------|-----|---|
| Correlações (A&Y + Deckwer) | 0,055 | — | 0,0135 | 0,70 | 0,0056 | 0,0147 | 0,32 | 0,66 |
| Shah + Deckwer | 0,055 | — | 0,0189 | 0,50 | 0,0063 | 0,0147 | 0,32 | 0,66 |
| CFD 2 (uniforme) | 0,086 | 104 | 0,0365 | 0,25 | 0,0073 | 0,0003 | 14,6 | 0,80 |
| CFD 3 (parabólico) | 0,088 | 106 | 0,0369 | 0,25 | 0,0073 | 0,0013 | 3,8 | 0,75 |
| **CFD 4 (parab. + lift)** | **0,086** | **103** | **0,0363** | **0,25** | **0,0073** | **0,0042** | **1,2** | **0,70** |

Com Da = 1,8, os limites são X_CSTR = 0,64 e X_PFR = 0,84.

**Leitura:**

- **Taxa global** (`1/k_ef = 1/kLa + 1/(k1 εL)`). O CFD dá kLa 2–3× maior que as correlações, porque tem εG maior e kL de Higbie. No exemplo (k1εL/kLa ≈ 0,25–0,7, regime misto), a taxa global muda +30 %. Para reações mais rápidas (k1 ≳ 0,1 1/s, ainda com Ha < 0,3), a taxa fica **controlada pela TM** e a diferença chega a 2–3×, ou seja, um volume de reator 2–3× diferente. Para reações lentas (k1 ≲ 10⁻³), a hidrodinâmica não importa. Isso define *quando* o CFD é necessário.
- **Conversão.** D_L estimado a partir da circulação do CFD (D_L ≈ 0,31·V_c·D, Joshi 1980) leva X de 0,66 (D_L de Deckwer, quase CSTR) para 0,70–0,80 conforme a circulação. A circulação que o CFD resolve é o que posiciona o reator entre CSTR e PFR.
- **Ressalvas.** (i) kL de Higbie vale para interface móvel; em água contaminada o kL real é menor, então o kLa do CFD é um limite superior. (ii) O 2D axissimétrico subestima a circulação (seção 4), e portanto subestima D_L e superestima X. O valor "verdadeiro" deve ficar entre o CFD 4 e as correlações. (iii) A constante de Joshi (0,31) precisa ser conferida no original.

## 6. Pendências / próximos passos

- [ ] Pontos de U_G = 1 e 4 cm/s (α na entrada = 0,05 e 0,20) para a curva εG × U_G
- [ ] Caso 3D (malha de 7,5 mm) para o vídeo da pluma e a circulação real
- [x] Dados experimentais recentes em `dados_experimentais.csv` (Mudde 2009 / Draw & Rzehak 2024; Besagni & Inzoli 2016)
- [ ] (Opcional) S-Gamma para a distribuição de tamanho de bolhas

> Observação sobre os perfis: a vazão líquida na seção da rodada 4 dá +13 % da vazão ascendente (o ideal seria ≈ 0). Isso indica que a média de 18 s (~2 voltas de circulação) ainda carrega incerteza estatística nos perfis locais. O εG global não é afetado.

---

## 7. Caso 3D (rodada 5): mesma física da rodada 4

Figura: `Programacao/coluna_bolhas/resultados/fig_2D_vs_3D.png`, script `figura_2D_vs_3D.py`. Dados em `resultados_cfd_3D/`.

**Configuração:** cilindro 3D, D = 0,15 m, H = 1,2 m, H0 = 0,9 m. Malha Trimmer de 7,5 mm (~50 mil células). Aspersor parabólico (média de α = 0,1 a 0,2 m/s, ou seja U_G = 2 cm/s), d = 5 mm, lift −0,05, Mixture k-ε. Simulado até **t = 28,8 s**; média temporal de 15 a 28,8 s.

| Grandeza | 2D (rodada 4) | **3D (rodada 5)** | Experimento / referência |
|----------|---------------|-------------------|--------------------------|
| εG global | 0,0856 | **0,0889 ± 0,0001** | Mudde (agulhas) 0,089 · Besagni (spider) 0,069 |
| α no eixo / na parede | 0,081–0,086 / 0,067–0,075 | 0,091 / 0,081 | — |
| V_L no eixo | +0,056 m/s | **+0,059 m/s** | Riquarts 0,25 m/s · Mudde 0,004–0,02 m/s |
| V_L junto à parede | −0,09 m/s | −0,08 m/s (−0,06 a −0,11 entre raios) | — |
| Inversão do V_L | r/R = 0,70 | r/R ≈ 0,61 | ≈ 0,7 |

**Leitura:**

1. **O 3D confirmou o 2D:** εG mudou só 4 % (0,086 → 0,089) e a circulação ficou praticamente igual. O 2D axissimétrico **não** era o responsável pela circulação fraca.
2. **A coluna ficou quase estacionária também em 3D** (σ do holdup = 0,0001). Não apareceu uma pluma serpenteando. Com bolhas de 5 mm, aspersor distribuído e k-ε (RANS), o escoamento fica no regime homogêneo, sem estruturas de grande escala. A literatura atribui a dinâmica forte a bolhas maiores que ~5,8 mm (lift negativo, Lucas et al. 2005; Draw & Rzehak 2024, Tab. 6) e/ou a modelos de turbulência menos dissipativos (LES).
3. **Validação:** εG em 3D coincide com o experimento de aspersor uniforme (**Mudde: 0,089, desvio < 1 %**). O modelo representa bem uma coluna homogênea com aspersor fino, e não a coluna com aspersor grosseiro de Besagni (0,069). Para esta seriam necessários a geometria do *spider* e a distribuição de tamanhos de bolha (S-Gamma ou duas classes).
4. **Estatística:** a média de 15 a 28,8 s (~1,5 volta de circulação) ainda mostra assimetria entre os 4 raios (faixa sombreada) e uma vazão líquida diferente de zero na sonda. **Os perfis locais são indicativos.** O εG global é robusto.

**Mensagem para a apresentação:** *"Em 2D ou em 3D, o modelo reproduz a coluna homogênea com aspersor uniforme (−3 % e < 1 %). A diferença em relação às correlações clássicas vem do aspersor e do tamanho das bolhas, não da dimensionalidade do modelo."* Isso leva a três próximos passos: S-Gamma (tamanho de bolha calculado), geometria real do aspersor e LES para a dinâmica da pluma.
