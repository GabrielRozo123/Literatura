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

## 4. Conclusões para o seminário

1. **O diâmetro de bolha controla εG.** De 1 mm para 5 mm, εG cai pela metade (0,172 → 0,086). Num modelo monodisperso, o diâmetro é um *dado de entrada*. Isso motiva modelos de balanço populacional (S-Gamma).
2. **O aspersor e as forças entre as fases controlam a circulação.** A mesma vazão de gás produz desde nenhuma circulação (rodada 2) até ~0,09 m/s com inversão em r/R = 0,7 (rodada 4). A circulação é a origem física do D_L do modelo de dispersão axial, que entra na equação de projeto (Pe ≈ 0,3, ou seja, a fase líquida se comporta quase como um CSTR).
3. **εG global é pouco sensível à circulação no 2D** (0,086–0,088 nas rodadas 2 a 4). O principal motivo de ele ficar acima de Akita & Yoshida e de Hikita é o diâmetro de bolha suposto. As correlações foram ajustadas em colunas reais, com distribuição de tamanhos e regiões heterogêneas.
4. **Limitação do 2D axissimétrico.** A circulação no eixo (0,06–0,09 m/s) ficou cerca de 3× abaixo de Riquarts (0,25 m/s). A pluma oscilante, que alimenta a circulação real, só existe em 3D.
5. **Lição numérica.** A primeira tentativa, com ar puro (α = 1) no fundo inteiro, formou uma camada de gás instável e divergiu. A condição de contorno tem de respeitar a física do aspersor.

## 5. Pendências / próximos passos

- [ ] Pontos de U_G = 1 e 4 cm/s (α na entrada = 0,05 e 0,20) para a curva εG × U_G
- [ ] Caso 3D (malha de 7,5 mm) para o vídeo da pluma e a circulação real
- [ ] Dados experimentais recentes em `dados_experimentais.csv` (artigos na pasta 07, a baixar via CAPES)
- [ ] (Opcional) S-Gamma para a distribuição de tamanho de bolhas

> Observação sobre os perfis: a vazão líquida líquida na seção da rodada 4 dá +13 % da vazão ascendente (o ideal seria ≈ 0). Isso indica que a média de 18 s (~2 voltas de circulação) ainda carrega incerteza estatística nos perfis locais. O εG global não é afetado.
