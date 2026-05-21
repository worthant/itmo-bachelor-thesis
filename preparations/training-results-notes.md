## неутешительные результаты по тренировке дополнительных моделей и simd

0. По итогу обучения получились вот такие модели. Они структурированно у меня
   есть в архиве и я их модульно и гибко умею загружать быстро на плату:

```csv
f176_b2_qat	176	2	qat	TRUE	very shallow	77804	95.59460760712565	377.0224609375	2026-05-16T12:20:20+00:00	95.54646124217622	101.3359375
f96_b6_ptq	96	6	ptq	TRUE	PTQ on small model	70476	95.47424169475205	431.6142578125	2026-05-16T11:58:40+00:00	95.49831487722676	107.3671875
f96_b6_qat	96	6	qat	TRUE	small-mid, aligned	70476	95.47424169475205	431.6142578125	2026-05-16T11:09:07+00:00	95.20943668753009	107.5703125
f128_b6_qat	128	6	qat	TRUE	mid, aligned	118540	95.88348579682234	619.4365234375	2026-05-16T11:13:25+00:00	95.54646124217622	164.3046875
f176_b4_qat	176	4	qat	TRUE	shallow	145740	96.1482908040443	684.3583984375	2026-05-16T12:24:44+00:00	95.73904670197399	186.5859375
f176_b5_qat	176	5	qat	TRUE	medium-shallow	179708	96.17236398651902	837.3662109375	2026-05-16T12:29:46+00:00	96.02792489167068	229.2109375
f160_b6_qat	160	6	qat	TRUE	aligned, below baseline	178892	95.95570534424651	855.1865234375	2026-05-16T11:19:14+00:00	96.12421762156957	232.9921875
f168_b6_qat	168	6	qat	TRUE	aligned, slightly below baseline	195900	96.10014443909485	921.6240234375	2026-05-16T11:24:38+00:00	95.85941261434762	252.0390625
f172_b6_ptq	172	6	ptq	FALSE	PTQ on baseline (172, not aligned)	204692	95.8353394318729	955.9677734375	2026-05-16T12:04:21+00:00	95.59460760712565	261.59375
f172_b6_qat	172	6	qat	FALSE	BASELINE: Hello Edge DS-CNN-M (NOT aligned)	204692	95.64275397207511	955.9677734375	2026-05-16T11:30:01+00:00	95.66682715454982	261.84375
f176_b6_ptq	176	6	ptq	TRUE	PTQ on aligned baseline	213676	95.71497351949928	991.0615234375	2026-05-16T12:10:11+00:00	95.57053442465094	271.5859375
f176_b6_qat	176	6	qat	TRUE	aligned, just above baseline	213676	96.24458353394319	991.0615234375	2026-05-16T11:35:39+00:00	96.19643716899374	271.8359375
f184_b6_qat	184	6	qat	TRUE	aligned, above baseline	232220	95.88348579682234	1063.4990234375	2026-05-16T11:41:36+00:00	95.76311988444873	292.3828125
f192_b6_ptq	192	6	ptq	TRUE	PTQ on larger aligned model	251532	95.90755897929706	1138.9365234375	2026-05-16T12:16:42+00:00	95.90755897929706	313.4296875
f192_b6_qat	192	6	qat	TRUE	aligned, above baseline	251532	96.02792489167068	1138.9365234375	2026-05-16T11:47:51+00:00	96.12421762156957	313.6796875
f176_b7_qat	176	7	qat	TRUE	deep	247644	96.17236398651902	1145.0302734375	2026-05-16T12:35:59+00:00	96.29272989889263	314.4609375
f176_b8_qat	176	8	qat	TRUE	very deep	281612	96.29272989889263	1298.3583984375	2026-05-16T12:42:37+00:00	96.07607125662012	357.0859375
f224_b6_qat	224	6	qat	TRUE	large, aligned (top of range)	336460	95.88348579682234	1470.6865234375	2026-05-16T11:54:35+00:00	95.69090033702456	406.3671875
f64_b6_qat	64	6	qat	TRUE	small, aligned	34700	94.92055849783341	291.8642578125	2026-05-16T11:04:51+00:00	94.46316803081368	62.8828125
slug	filters	blocks	quant	simd_aligned	description	params	fp32_acc_pct	fp32_size_kb	train_date_utc	int8_acc_pct	int8_size_kb
```

дальше начался ад с тем, что мне не понравилось время их работы. мало того что
accuracy не то что бы крутая, дак ещё и работают большие модели по секунде.
дальше будут мои страдания, замеры и выводы:

1. Потратил несколько часов на то, что переместил `esp-tflite-micro` как
   компонент себе в проект, убрал его из dependencies, добавил append pub_req
   esp_nn, скопировал к себе всю директорию, .bak

По итогу, это позволило мне получать изнутри него из conv.cc логи для свёрток.
Таким образом я убедился в том что для 176 фильтров ch_mod8=0, то есть scratch
выделен, свёртки действительно 1x1. все условия fast path. и при этом, всё равно
PW занимает 155мс для той же f176_b6 модели.

2. Я увеличивал iram и dram - на скорость особо не влияло. даже наоборот, когда
   увеличивал - инференс становился медленнее

вот например когда iram=16кб и dram=32кб, лог для `f176_b2_qat`:

```
I (1900) mfcc: ok  win=640 stride=320 fft=1024 mel=40 coeff=10 frames=49
I (1900) kws: build sanity: icache=16 kB dcache=32 kB
I (1910) kws: before arena: free_internal=335KB largest_block=244KB needed=140KB
I (1920) kws: free internal: 195 KB  free PSRAM: 8174 KB
I (1920) kws: model loaded  arena_used=108232/143360
I (1930) kws: input:  type=9 dims=[1,49,10,1] scale=0.634640 zp=67
I (1930) kws: output: type=9 dims=[1,12] scale=0.041735 zp=-34
I (1940) kws: model size: 103768 bytes
I (2000) prof_storage: spiffs ok  total=1404596 used=37901
I (4520) ve_kws: recorded 2466ms
I (4970) ve_kws: MFCC 351ms
I (5030) kws: tensor diagnostics:
I (5030) kws:   input[0]: data=0x3fcae750 bytes=490 (internal=1 psram=0)
I (5030) kws:   arena: 0x3fcac2fc (internal=1 psram=0)
I (5040) kws:   model_data: 0x3c0741c0 (internal=0 psram=0 flash=1)
E (5040) CONV_DBG: [0] in=10x49x1 filter=4x10 out=5x25x176 buf_idx=0 in_zp=-67 ch_mod8=1
E (5160) CONV_DBG: [1] in=5x25x176 filter=1x1 out=5x25x176 buf_idx=2 in_zp=128 ch_mod8=0
E (5330) CONV_DBG: [2] in=5x25x176 filter=1x1 out=5x25x176 buf_idx=4 in_zp=128 ch_mod8=0
I (5510) kws: invoke cycles: 111836485 (466.0 ms @ 240 MHz)
I (5510) kws: result: _silence_ (2.6710)
```

вот настройки кеша:

```
#
# Cache config
#
CONFIG_ESP32S3_INSTRUCTION_CACHE_16KB=y
# CONFIG_ESP32S3_INSTRUCTION_CACHE_32KB is not set
CONFIG_ESP32S3_INSTRUCTION_CACHE_SIZE=0x4000
# CONFIG_ESP32S3_INSTRUCTION_CACHE_4WAYS is not set
CONFIG_ESP32S3_INSTRUCTION_CACHE_8WAYS=y
CONFIG_ESP32S3_ICACHE_ASSOCIATED_WAYS=8
# CONFIG_ESP32S3_INSTRUCTION_CACHE_LINE_16B is not set
CONFIG_ESP32S3_INSTRUCTION_CACHE_LINE_32B=y
CONFIG_ESP32S3_INSTRUCTION_CACHE_LINE_SIZE=32
# CONFIG_ESP32S3_DATA_CACHE_16KB is not set
CONFIG_ESP32S3_DATA_CACHE_32KB=y
# CONFIG_ESP32S3_DATA_CACHE_64KB is not set
CONFIG_ESP32S3_DATA_CACHE_SIZE=0x8000
# CONFIG_ESP32S3_DATA_CACHE_4WAYS is not set
CONFIG_ESP32S3_DATA_CACHE_8WAYS=y
CONFIG_ESP32S3_DCACHE_ASSOCIATED_WAYS=8
# CONFIG_ESP32S3_DATA_CACHE_LINE_16B is not set
CONFIG_ESP32S3_DATA_CACHE_LINE_32B=y
# CONFIG_ESP32S3_DATA_CACHE_LINE_64B is not set
CONFIG_ESP32S3_DATA_CACHE_LINE_SIZE=32
# end of Cache config

```

а вот например когда я меняю настройки dram=64кб:

```
#
# Cache config
#
CONFIG_ESP32S3_INSTRUCTION_CACHE_16KB=y
# CONFIG_ESP32S3_INSTRUCTION_CACHE_32KB is not set
CONFIG_ESP32S3_INSTRUCTION_CACHE_SIZE=0x4000
# CONFIG_ESP32S3_INSTRUCTION_CACHE_4WAYS is not set
CONFIG_ESP32S3_INSTRUCTION_CACHE_8WAYS=y
CONFIG_ESP32S3_ICACHE_ASSOCIATED_WAYS=8
# CONFIG_ESP32S3_INSTRUCTION_CACHE_LINE_16B is not set
CONFIG_ESP32S3_INSTRUCTION_CACHE_LINE_32B=y
CONFIG_ESP32S3_INSTRUCTION_CACHE_LINE_SIZE=32
# CONFIG_ESP32S3_DATA_CACHE_16KB is not set
# CONFIG_ESP32S3_DATA_CACHE_32KB is not set
CONFIG_ESP32S3_DATA_CACHE_64KB=y
CONFIG_ESP32S3_DATA_CACHE_SIZE=0x10000
# CONFIG_ESP32S3_DATA_CACHE_4WAYS is not set
CONFIG_ESP32S3_DATA_CACHE_8WAYS=y
CONFIG_ESP32S3_DCACHE_ASSOCIATED_WAYS=8
CONFIG_ESP32S3_DATA_CACHE_LINE_32B=y
# CONFIG_ESP32S3_DATA_CACHE_LINE_64B is not set
CONFIG_ESP32S3_DATA_CACHE_LINE_SIZE=32
# end of Cache config
```

для той же модели:

```
I (1885) mfcc: ok  win=640 stride=320 fft=1024 mel=40 coeff=10 frames=49
I (1885) kws: build sanity: icache=16 kB dcache=64 kB
I (1895) kws: before arena: free_internal=304KB largest_block=244KB needed=140KB
I (1905) kws: free internal: 164 KB  free PSRAM: 8174 KB
I (1905) kws: model loaded  arena_used=108244/143360
I (1915) kws: input:  type=9 dims=[1,49,10,1] scale=0.634640 zp=67
I (1915) kws: output: type=9 dims=[1,12] scale=0.041735 zp=-34
I (1925) kws: model size: 103768 bytes
I (1985) prof_storage: spiffs ok  total=1404596 used=37901
I (4505) ve_kws: recorded 2466ms
I (4945) ve_kws: MFCC 343ms
I (5005) kws: tensor diagnostics:
I (5005) kws:   input[0]: data=0x3fcae730 bytes=490 (internal=1 psram=0)
I (5005) kws:   arena: 0x3fcac2d8 (internal=1 psram=0)
I (5015) kws:   model_data: 0x3c0741c0 (internal=0 psram=0 flash=1)
E (5015) CONV_DBG: [0] in=10x49x1 filter=4x10 out=5x25x176 buf_idx=0 in_zp=-67 ch_mod8=1
E (5135) CONV_DBG: [1] in=5x25x176 filter=1x1 out=5x25x176 buf_idx=2 in_zp=128 ch_mod8=0
E (5305) CONV_DBG: [2] in=5x25x176 filter=1x1 out=5x25x176 buf_idx=4 in_zp=128 ch_mod8=0
I (5485) kws: invoke cycles: 111575815 (464.9 ms @ 240 MHz)
I (5485) kws: result: up (1.1268)
I (5485) ve_kws: inf=475ms -> up (1.127)
```

ну то есть чуть инференс ускорился, но не то что бы это сильно на что-то влияет.
iram аналогично.

3. Попробовал упаковать модели в dram. для этого просто добавил в массив вот
   такую метку:

```c
__attribute__((aligned(16), section(".dram1.data")))
const unsigned char g_model_data[] = {...};
```

по итогу почти ничего не влезло, кроме f176_b2_qat и f64_b6_qat, потому что:

N8R8 — это 8 МБ flash + 8 МБ PSRAM. У ESP32-S3 чипа есть:

512 КБ internal SRAM (это много, но из них ~150 КБ занято IDF runtime, FreeRTOS,
драйверами, твоим основным кодом). 8 МБ PSRAM (быстро, но через интерфейс). 8 МБ
flash (только для чтения, через cache).

для большой модели в логе: free_internal=288KB largest_block=228KB. То есть в
MALLOC_CAP_INTERNAL свободно 288 КБ. Модель 268 КБ. Можно влезть впритык, но
нужен непрерывный блок 268 КБ, а самый большой = 228 КБ. Фрагментация.

по итогу я шёл по убыванию размера, вот эти все не впихнулись:

```csv
f96_b6_ptq    96    6    ptq    TRUE    PTQ on small model    70476    95.47424169475205    431.6142578125    2026-05-16T11:58:40+00:00    95.49831487722676    107.3671875
f96_b6_qat    96    6    qat    TRUE    small-mid, aligned    70476    95.47424169475205    431.6142578125    2026-05-16T11:09:07+00:00    95.20943668753009    107.5703125
f128_b6_qat    128    6    qat    TRUE    mid, aligned    118540    95.88348579682234    619.4365234375    2026-05-16T11:13:25+00:00    95.54646124217622    164.3046875
f176_b4_qat    176    4    qat    TRUE    shallow    145740    96.1482908040443    684.3583984375    2026-05-16T12:24:44+00:00    95.73904670197399    186.5859375
f176_b5_qat    176    5    qat    TRUE    medium-shallow    179708    96.17236398651902    837.3662109375    2026-05-16T12:29:46+00:00    96.02792489167068    229.2109375
```

потому что tf arena вот эта должна я так понял выделяться подряд. а там память
вся фрагментирована жесть. получается что место вроде есть но свободного блока
под неё не находилось, поэтому вот.

и при этом я запускаю щас f176_b2_qat модель, вот эту:

```csv
f176_b2_qat	176	2	qat	TRUE	very shallow	77804	95.59460760712565	377.0224609375	2026-05-16T12:20:20+00:00	95.54646124217622	101.3359375
```

она ведь маленькая. а ранится аж 472ms. ужас.

вот лог:

```
--- Terminal on /dev/ttyACM1 | 9600 8-N-1
--- Available filters and text transformations: debug, default, direct, esp32_exception_decoder, hexl
ify, log2file, nocontrol, printable, send_on_enter, time
--- More details at https://bit.ly/pio-monitor-filters
--- Quit: Ctrl+C | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H
I (1829) main: sound wakeup -> inference (boot 249ms)
I (1829) i2s_mic: --- i2s init START ---
D (1829) i2s_common: rx channel is registered on I2S0 successfully
D (1829) i2s_common: DMA malloc info: dma_desc_num = 6, dma_desc_buf_size = dma_frame_num * slot_num
* data_bit_width = 960
D (1839) i2s_std: Clock division info: [sclk] 160000000 Hz [mdiv] 39 [mclk] 4096000 Hz [bdiv] 4 [bclk
] 1024000 Hz
D (1849) gdma: new pair (0,1) at 0x3fcc4c98
D (1859) gdma: new rx channel (0,1) at 0x3fcc4c5c
D (1859) intr_alloc: Connected src 67 to int 13 (cpu 0)
D (1869) gdma: install interrupt service for rx channel (0,1)
D (1869) i2s_std: The rx channel on I2S0 has been initialized to STD mode successfully
D (1879) i2s_common: i2s rx channel enabled
I (1879) i2s_mic: --- i2s init DONE ---
I (1889) mfcc: ok  win=640 stride=320 fft=1024 mel=40 coeff=10 frames=49
I (1889) kws: build sanity: icache=16 kB dcache=32 kB
I (1899) kws: before arena: free_internal=235KB largest_block=144KB needed=140KB
I (1909) kws: free internal: 91 KB  free PSRAM: 8174 KB
I (1909) kws: model loaded  arena_used=108232/143360
I (1919) kws: input:  type=9 dims=[1,49,10,1] scale=0.634640 zp=67
I (1919) kws: output: type=9 dims=[1,12] scale=0.041735 zp=-34
I (1929) kws: model size: 103768 bytes
I (1989) prof_storage: spiffs ok  total=1404596 used=37901
I (4509) ve_kws: recorded 2467ms
I (4959) ve_kws: MFCC 351ms
I (5019) kws: tensor diagnostics:
I (5019) kws:   input[0]: data=0x3fcc79a0 bytes=490 (internal=1 psram=0)
I (5019) kws:   arena: 0x3fcc554c (internal=1 psram=0)
I (5029) kws:   model_data: 0x3fc986a0 (internal=1 psram=0 flash=0)
E (5029) CONV_DBG: [0] in=10x49x1 filter=4x10 out=5x25x176 buf_idx=0 in_zp=-67 ch_mod8=1
E (5149) CONV_DBG: [1] in=5x25x176 filter=1x1 out=5x25x176 buf_idx=2 in_zp=128 ch_mod8=0
E (5319) CONV_DBG: [2] in=5x25x176 filter=1x1 out=5x25x176 buf_idx=4 in_zp=128 ch_mod8=0
I (5489) kws: invoke cycles: 110966188 (462.4 ms @ 240 MHz)
I (5489) kws: result: _silence_ (1.7946)
I (5489) ve_kws: inf=472ms -> _silence_ (1.795)
I (5549) ve_kws: no keyword (_silence_ 1.795)
I (5549) main: total pipeline: 3561ms
I (9099) vad_sleep: sleep LED on
I (9099) vad_sleep: entering deep sleep
Disconnected ([Errno 5] Input/output error)
Reconnecting to /dev/ttyACM1     Connected!
(867) memory_layout: Reserved memory range 0x40374000 - 0x40387c00
D (874) memory_layout: Reserved memory range 0x600fe000 - 0x600fe120
D (880) memory_layout: Reserved memory range 0x600fffe8 - 0x60100000
D (886) memory_layout: Building list of available memory regions:
D (892) memory_layout: Available memory region 0x3fcb6430 - 0x3fcc0000
D (898) memory_layout: Available memory region 0x3fcc0000 - 0x3fcd0000
D (904) memory_layout: Available memory region 0x3fcd0000 - 0x3fce0000
D (910) memory_layout: Available memory region 0x3fce0000 - 0x3fce9710
D (917) memory_layout: Available memory region 0x3fce9710 - 0x3fceee34
D (923) memory_layout: Available memory region 0x3fcf0000 - 0x3fcf8000
D (929) memory_layout: Available memory region 0x600fe120 - 0x600fffe8
I (935) heap_init: Initializing. RAM available for dynamic allocation:
D (942) heap_init: New heap initialised at 0x3fcb6430
I (946) heap_init: At 3FCB6430 len 000332E0 (204 KiB): RAM
I (951) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
D (957) heap_init: New heap initialised at 0x3fcf0000
I (961) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
D (967) heap_init: New heap initialised at 0x600fe120
I (971) heap_init: At 600FE120 len 00001EC8 (7 KiB): RTCRAM
D (977) cpu_start: calling init function: 0x420246cc on core: 0
D (982) cpu_start: calling init function: 0x42026ac8 on core: 0
D (988) cpu_start: calling init function: 0x420224d8 on core: 0
I (994) esp_psram: Adding pool of 8192K of PSRAM memory to heap allocator
D (1000) cpu_start: calling init function: 0x42022a68 on core: 0
D (1006) intr_alloc: Connected src 39 to int 1 (cpu 0)
D (1011) cpu_start: calling init function: 0x42022a74 on core: 0
D (1016) cpu_start: calling init function: 0x4201f724 on core: 0
D (1022) cpu_start: calling init function: 0x42020318 on core: 0
D (1028) cpu_start: calling init function: 0x42028034 on core: 0
D (1034) cpu_start: calling init function: 0x420249f8 on core: 0
```

4. сделал замеры - собрал статистику профилирования по слоям для нескольких
   моделек и вот что вышло:

- [x] **f64_b6_qat**
  - [x] `measurements/profile/profile_f64_b6_qat.csv`
  - [x] `measurements/energy/energy_f64_b6_qat.csv`
  - [x] `measurements/stats/stats_f64_b6_qat.csv`

- [x] **f96_b6_qat**
  - [x] `measurements/profile/profile_f96_b6_qat.csv`
  - [x] `measurements/energy/energy_f96_b6_qat.csv`
  - [x] `measurements/stats/stats_f96_b6_qat.csv`

- [x] **f128_b6_qat**
  - [x] `measurements/profile/profile_f128_b6_qat.csv`
  - [x] `measurements/energy/energy_f128_b6_qat.csv`
  - [x] `measurements/stats/stats_f128_b6_qat.csv`

- [x] **f160_b6_qat**
  - [x] `measurements/profile/profile_f160_b6_qat.csv`
  - [x] `measurements/energy/energy_f160_b6_qat.csv`
  - [x] `measurements/stats/stats_f160_b6_qat.csv`

- [x] **f96_b6_ptq**
  - [x] `measurements/profile/profile_f96_b6_ptq.csv`
  - [x] `measurements/energy/energy_f96_b6_ptq.csv`
  - [x] `measurements/stats/stats_f96_b6_ptq.csv`

stats f64 b6 qat:

```csv
op_index,op_tag,mean_ms,std_ms,min_ms,max_ms,median_ms,pct_time
0,CONV_2D,39.752,0.004,39.745,39.767,39.751,19.421
1,DEPTHWISE_CONV_2D,1.441,0.007,1.433,1.466,1.438,0.704
2,CONV_2D,25.195,3.942,24.785,64.021,24.798,12.309
3,DEPTHWISE_CONV_2D,1.473,0.003,1.467,1.481,1.472,0.720
4,CONV_2D,25.211,3.925,24.805,64.064,24.818,12.317
5,DEPTHWISE_CONV_2D,1.440,0.008,1.434,1.471,1.438,0.704
6,CONV_2D,24.835,0.005,24.825,24.851,24.835,12.133
7,DEPTHWISE_CONV_2D,1.451,0.007,1.441,1.479,1.449,0.709
8,CONV_2D,25.172,3.901,24.769,63.989,24.783,12.298
9,DEPTHWISE_CONV_2D,1.465,0.004,1.460,1.476,1.464,0.716
10,CONV_2D,24.828,0.006,24.814,24.848,24.827,12.130
11,DEPTHWISE_CONV_2D,1.439,0.008,1.433,1.467,1.436,0.703
12,CONV_2D,25.230,3.940,24.824,64.033,24.833,12.326
13,MEAN,5.683,0.004,5.675,5.687,5.682,2.776
14,FULLY_CONNECTED,0.071,0.001,0.069,0.077,0.071,0.035

```

stats f96_b6_qat:

```csv
op_index,op_tag,mean_ms,std_ms,min_ms,max_ms,median_ms,pct_time
0,CONV_2D,59.625,0.002,59.619,59.629,59.626,15.080
1,DEPTHWISE_CONV_2D,2.202,0.004,2.199,2.211,2.200,0.557
2,CONV_2D,52.579,5.518,51.788,91.011,51.794,13.298
3,DEPTHWISE_CONV_2D,2.201,0.004,2.197,2.211,2.199,0.557
4,CONV_2D,52.197,3.921,51.799,91.016,51.805,13.202
5,DEPTHWISE_CONV_2D,2.213,0.004,2.208,2.223,2.211,0.560
6,CONV_2D,52.177,3.921,51.779,90.996,51.785,13.197
7,DEPTHWISE_CONV_2D,2.211,0.003,2.208,2.220,2.209,0.559
8,CONV_2D,52.568,5.519,51.776,91.021,51.782,13.295
9,DEPTHWISE_CONV_2D,2.204,0.004,2.200,2.214,2.202,0.557
10,CONV_2D,51.795,0.003,51.787,51.802,51.794,13.100
11,DEPTHWISE_CONV_2D,2.206,0.004,2.200,2.216,2.204,0.558
12,CONV_2D,52.593,5.516,51.802,91.016,51.809,13.302
13,MEAN,8.514,0.003,8.508,8.520,8.514,2.153
14,FULLY_CONNECTED,0.097,0.001,0.096,0.102,0.097,0.025

```

stats f96_b6_ptq:

```csv
op_index,op_tag,mean_ms,std_ms,min_ms,max_ms,median_ms,pct_time
0,CONV_2D,59.636,0.002,59.629,59.639,59.636,15.083
1,DEPTHWISE_CONV_2D,2.211,0.004,2.207,2.220,2.208,0.559
2,CONV_2D,52.583,5.517,51.793,91.010,51.798,13.299
3,DEPTHWISE_CONV_2D,2.206,0.003,2.202,2.215,2.205,0.558
4,CONV_2D,52.178,3.921,51.780,90.998,51.786,13.196
5,DEPTHWISE_CONV_2D,2.204,0.005,2.199,2.216,2.201,0.557
6,CONV_2D,52.194,3.921,51.790,91.014,51.802,13.200
7,DEPTHWISE_CONV_2D,2.212,0.003,2.204,2.221,2.210,0.559
8,CONV_2D,52.567,5.519,51.776,91.019,51.782,13.295
9,DEPTHWISE_CONV_2D,2.204,0.003,2.201,2.215,2.204,0.557
10,CONV_2D,51.799,0.003,51.793,51.808,51.799,13.101
11,DEPTHWISE_CONV_2D,2.207,0.004,2.203,2.217,2.204,0.558
12,CONV_2D,52.577,5.517,51.785,91.003,51.792,13.297
13,MEAN,8.516,0.002,8.508,8.521,8.516,2.154
14,FULLY_CONNECTED,0.104,0.001,0.101,0.109,0.104,0.026
```

stats f128_b6_ptq:

```csv
op_index,op_tag,mean_ms,std_ms,min_ms,max_ms,median_ms,pct_time
0,CONV_2D,80.270,5.517,79.476,118.695,79.487,12.463
1,DEPTHWISE_CONV_2D,2.933,0.004,2.928,2.941,2.934,0.455
2,CONV_2D,88.790,3.921,88.389,127.612,88.400,13.786
3,DEPTHWISE_CONV_2D,2.937,0.004,2.930,2.948,2.938,0.456
4,CONV_2D,89.585,6.723,88.399,127.624,88.410,13.909
5,DEPTHWISE_CONV_2D,2.940,0.004,2.935,2.949,2.941,0.457
6,CONV_2D,88.773,3.921,88.374,127.593,88.381,13.783
7,DEPTHWISE_CONV_2D,2.945,0.004,2.940,2.953,2.945,0.457
8,CONV_2D,89.167,5.517,88.374,127.596,88.384,13.845
9,DEPTHWISE_CONV_2D,2.937,0.004,2.932,2.945,2.938,0.456
10,CONV_2D,89.179,5.519,88.384,127.623,88.395,13.846
11,DEPTHWISE_CONV_2D,2.938,0.004,2.932,2.948,2.938,0.456
12,CONV_2D,89.196,5.517,88.404,127.622,88.412,13.849
13,MEAN,11.346,0.004,11.340,11.356,11.345,1.762
14,FULLY_CONNECTED,0.121,0.001,0.120,0.126,0.121,0.019
```

stats f160_b6_ptq:

```csv
op_index,op_tag,mean_ms,std_ms,min_ms,max_ms,median_ms,pct_time
0,CONV_2D,99.345,0.003,99.338,99.351,99.344,10.423
1,DEPTHWISE_CONV_2D,3.661,0.004,3.655,3.668,3.661,0.384
2,CONV_2D,136.639,8.593,134.670,173.920,134.676,14.336
3,DEPTHWISE_CONV_2D,3.666,0.004,3.660,3.675,3.667,0.385
4,CONV_2D,135.226,0.014,135.201,135.242,135.234,14.188
5,DEPTHWISE_CONV_2D,3.678,0.005,3.671,3.688,3.680,0.386
6,CONV_2D,136.605,8.592,134.639,173.884,134.644,14.332
7,DEPTHWISE_CONV_2D,3.668,0.004,3.662,3.675,3.669,0.385
8,CONV_2D,135.181,0.010,135.157,135.190,135.184,14.183
9,DEPTHWISE_CONV_2D,3.671,0.005,3.664,3.681,3.671,0.385
10,CONV_2D,136.636,8.615,134.659,174.411,134.670,14.336
11,DEPTHWISE_CONV_2D,3.660,0.004,3.655,3.667,3.661,0.384
12,CONV_2D,136.761,7.758,135.161,174.959,135.190,14.349
13,MEAN,14.573,3.920,14.172,53.386,14.180,1.529
14,FULLY_CONNECTED,0.152,0.001,0.150,0.158,0.152,0.016
```

что отсюда можно заключить. работает всё до жути медленно. чем больше модель -
тем хуже, вообще переваливаем за секунду. быстро только на оч маленьких где
фильтров 64, ну от силы 96.

5. дальше я в нескольких чатах судорожно пытался как-то это пофиксить всё.
   нейронки постоянно лезли в интернет, находили статьи и высчитывали MAC из
   бенчмарков Espressif'а. И что самое смешное - каждый раз находили какие-то
   новые рандомные числа и приходили к разным выводам.

И вот этот момент надо быть унифицировать. найти КОНКРЕТНЫЕ источники, или взять
из уже имеющихся, я думал у нас таковых достаточно, конкретные цифры.

Из того что мне уже накидывали - там то esp32-p4 были, то какие-то официальные
бенчмарки espressif, то person detection. При чём постоянно цифры-то в них были
разные.

основной аргумент был в том что с esp-nn модель person detection в int8
квантизации на esp32-s3 без esp-nn работала 2300ms, а с - 54ms. на p4 - 1395ms
без esp-nn и 73ms с esp-nn

а дальше было много разные расчётов mac операций. если верить опять же
нейронкам, то у меня модель f176 должна почему-то иметь типа 25 mmac, т.е. 25
миллионов операций сложения и умножения.

При этом насколько я знаю, модельки для детекции людей как раз требуют 14-25
mmac, и весят в районе 250kb.

и вообще, мы блин распознаём звук. звука сука. и при этом мы ещё и
предобрабатываем его до жести что от него после DCT вообще ничего не остаётся
почти. ну не может быть так медленно. Тут я немножко в тупике. Все эти расчёты
mac и прикидки во сколько раз у меня модель медленнее или быстрее, сравнения с
edge impulse бенчмарком или с чем-то ещё, они ощущаются как галюцинации и
накидывание цифр. по факту конкретного ресёрча нету. ровно как и понимания у
меня нету почему модель так медленно работает, хотя я старался делал чтоб было
норм. 8 часов я проверял включены SIMD или нет.

- Добавили cycle counter через esp_cpu_get_cycle_count() вокруг Invoke(). Там
  видно что cpu реально работал столько циклов в логах.
- Подняли I-cache 16→32 КБ, D-cache 32→64 КБ. Тестили оба варианта line size (32
  и 64). Прирост незначительный.
- Копировали модель в psram через memcpy, не быстрее нихрена. В dram клали, то
  же самое.
- добавили с conv.cc логирование на входе в EvalQuantizedPerChannel: dims,
  buf_idx, in_zp_ch_mod8. Ну вот любуйся в логах, чем поможет-то. SIMD с виду
  работает. А скорости нету.
- макрос esp_nn определён, ветка активна
- конфиг компилятора optimisation perf=y у меня стоит. флаг у esp-nn стоит -O2.

непойму у нас просто модель такая тяжёлая или что за хрень? есть стойкое
ощущение что я последние пол года пока делал этот диплом нереально ошибался и
непонятно зачем тренировал огромные модели. а надо было просто сделать кучу
маленьких и на них тестить edge-ai

или возможно я как раз провёл хорошее исследование, и надо для научности
применить какой-нибудь Парето-анализ и сказать что вот я нашёл такую вот
модельку, достиг её по критериям оптимальности или эффективности конкретным, и
показать это в вкр и на защите диплома самой.
