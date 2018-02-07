import string
import GUI.Library as Library
import GUI.fit as fit

# generate a Netlist based on the input parameters and save it to ProjectHome/Netlist
class NetListGenerator:
    def generate(self, part, simulation, TID_level, output_option, output_filepath, netlist_filepath): # generate Netlist
        content = []
        # if part == Library.PARTS[0]:
        #     if simulation == Library.SIMULATION[0]:
        #         content = self.content_LT1175(TID_level, output_filepath)
        #     elif simulation == Library.SIMULATION[1]:
        #         content = self.content_LT1175_ABM(TID_level, output_filepath)
        # elif part == Library.PARTS[1]:
        #     if simulation == Library.SIMULATION[0]:
        #         content = self.content_AD590(TID_level, output_filepath)
        #     elif simulation == Library.SIMULATION[1]:
        #         content = self.content_AD590_ABM(TID_level, output_filepath)
        # Section 1: Title
        content.extend(['Title: ' + part + ' / ' + TID_level + ' / ' + 'T= 300.15K = 27C',
                        ''])
        # Section 2: Input Voltage Source
        content.extend(['*Input Voltage Source',
                        '***************'])
        content.extend(Library.INPUT_VOLTAGE_SOURCE[part])
        content.append('')
        # Section 3: Circuit core
        content.extend(['*Circuit Core',
                        '*************',])
        content.extend(Library.CIRCUIT_CORE[part])
        content.append('')

        # 2 additional sections for current source simulation
        if simulation == Library.SIMULATION_SOURCE:
            # Section Parameters (only if use current source):
            content.extend(['*Parameters',
                            '***********'])
            # a,b,c
            if part == Library.PART_AD590:
                paras = ['*PRE_RAD_PNP',
                         '.PARAM a1=-41.935',
                         '.PARAM b1=47.6314',
                         '.PARAM c1=-11.045',
                         '',
                         '*20krad_PNP',
                         '.PARAM a2=-32.249',
                         '.PARAM b2=35.6571',
                         '.PARAM c2=-9.1636',
                         '',
                         '*PRE_RAD_NPN',
                         '.PARAM a3=-39.91',
                         '.PARAM b3=40.6194',
                         '.PARAM c3=-4.4288',
                         '',
                         '*20krad_NPN',
                         '.PARAM a4=-34.92',
                         '.PARAM b4=30.4499',
                         '.PARAM c4=1.11115']
                content.extend(paras)
            elif part == Library.PART_LT1175:
                paras = ['*PRE_RAD',
                         '.PARAM a1=-39.30421',
                         '.PARAM b1=48.21879',
                         '.PARAM c1=-15.6477',
                         '',]
                if TID_level == Library.T2_5KRAD:
                    paras.extend(['*2.5krad',
                                  '.PARAM a2=-39.12298',
                                  '.PARAM b2=53.5479',
                                  '.PARAM c2=-21.84106'])
                elif TID_level == Library.T5KRAD:
                    paras.extend(['*5krad',
                                  '.PARAM a2=-38.8789',
                                  '.PARAM b2=59.74651',
                                  '.PARAM c2=-23.3925'])
                content.extend(paras)
            # scale
            content.append('')
            content.extend(Library.SCALE[part])
            content.append('')
            # Section Function (only if use current source):
            content.extend(['*Function'
                            '*********'])
            content.extend(Library.FUNCTIONS[part])
            content.append('')
        # Section 4: Input
        content.extend(['*Input',
                        '******',])
        content.extend(Library.INPUT[part])
        content.append('')
        # Section 5: Output
        content.extend(['*Output',
                        '*******',
                        '.print dc format=noindex file=' + output_filepath])
        content.extend(Library.OUTPUT[part][output_option])
        content.append('')
        # Section 6: Subcircuit
        content.extend(['*Subcircuit',
                        '************'])
        content.extend(Library.SUBCIRCUIT[part][simulation])
        content.extend(['*End Subcircuit',
                        ''])
        # Section 7: Library
        content.extend(['*Library',
                        '*******'])
        if simulation == Library.SIMULATION_MODEL:
            content.extend(Library.LIBRARY_TID_LEVEL_MODEL[TID_level])
        else:
            content.extend(Library.LIBRARY_TID_LEVEL_MODEL[Library.TPRE_RAD])
        if part == Library.PART_AD590:
            content.extend(['*JFET',
                            '.model NJF_TYP NJF (',
                            '+ VTO = -1.0	BETA = 6.2E-4	LAMBDA = 0.003',
                            '+ RD = 0.01      RS = 1e-4',
                            '+ CGS = 3E-12    CGD=1.5E-12     IS=5E-10)',
                            '']),
        content.extend(['',
                        '*end of the netlist',
                        '.end'])
        
        # print content to netlist file
        file = open(netlist_filepath, 'wb')
        for line in content:
            text = (line + '\r\n').encode('ascii')
            file.write(text)
        file.close()
        return

    def content_AD590(self, TID_level, output_filepath):
        content_AD590 = ['Title: AD590 / ' + TID_level + ' / T= 300.15K = 27C',
                         '*',
                         '',
                         '*Voltage Source',
                         'VIN 1 0 DC 0V',
                         '',
                         '*Umbrella circuit',
                         'X1 1 2 AD590_sc',
                         'ROUT 2 0 1m',
                         '',
                         '*Input',
                         '.dc VIN 0 30 0.01',
                         '',
                         '*Output',
                         # '.print dc format=noindex file=AD590_' + TID_level + '_27C_V1.txt',
                         '.print dc format=noindex file=' + output_filepath,
                         '+ V(1)',
                         '+ I(ROUT)',
                         '',
                         '*Subcircuit',
                         '.subckt AD590_sc IN OUT',
                         '',
                         '*Capacitance: C<name> <+ node> <- node> [model name] <value> + [IC=<initial value>]',
                         'c1 1 8 26p',
                         '',
                         '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                         'r1 IN 4 260',
                         'r2 IN 3 1040',
                         'r3 5 16 5000',
                         'r4 11 5 11000',
                         'r5 12 OUT 146',
                         'r6 15 OUT 820',
                         '',
                         '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                         'Q11 1 5 12 QNMOD 35 temp=27',
                         'Q10 5 5 12 QNMOD 35 temp=27',
                         'Q9 6 5 15 QNMOD 280 temp=27',
                         'Q6 7 7 IN QLPMOD 10 temp=27',
                         'Q4 1 8 4 QLPMOD 10 temp=27',
                         'Q3 1 8 4 QLPMOD 10 temp=27',
                         'Q5 8 8 3 QLPMOD 10 temp=27',
                         'Q2 6 8 4 QLPMOD 10 temp=27',
                         'Q1 6 8 4 QLPMOD 10 temp=27',
                         'Q7 7 6 11 QNMOD 10 temp=27',
                         'Q8 8 1 11 QNMOD 10 temp=27',
                         '',
                         '*JFET: J<name> <drain> <gate> <source> <model name> [area value]',
                         'J1 8 16 11 NJF_TYP',
                         '',
                         '*end of the subcircuit',
                         '.ends',
                         '',
                         '*Library', ]
        content_AD590.extend(Library.LIBRARY_TID_LEVEL_MODEL[TID_level])
        content_AD590.extend(['',
                              '*JFET',
                              '.model NJF_TYP NJF (',
                              '+ VTO = -1.0	BETA = 6.2E-4	LAMBDA = 0.003',
                              '+ RD = 0.01      RS = 1e-4',
                              '+ CGS = 3E-12    CGD=1.5E-12     IS=5E-10)',
                              '',
                              '*end of the netlist',
                              '.end'])
        return content_AD590

    def content_AD590_ABM(self, TID_level, output_filepath):
        content_AD590_ABM = ['Title: AD590 / ' + TID_level + ' / T= 300.15K = 27C',
                             '*',
                             '',
                             '*Voltage Source',
                             'VIN 2 0 DC 0V',
                             'VOUT 20 0 0',
                             '',
                             '*Parameters',
                             '***********',
                             '*PRE_RAD_PNP',
                             '.PARAM a1=-41.935',
                             '.PARAM b1=47.6314',
                             '.PARAM c1=-11.045',
                             '',
                             '*20krad_PNP',
                             '.PARAM a2=-32.249',
                             '.PARAM b2=35.6571',
                             '.PARAM c2=-9.1636',
                             '',
                             '*PRE_RAD_NPN',
                             '.PARAM a3=-39.91',
                             '.PARAM b3=40.6194',
                             '.PARAM c3=-4.4288',
                             '',
                             '*20krad_NPN',
                             '.PARAM a4=-34.92',
                             '.PARAM b4=30.4499',
                             '.PARAM c4=1.11115',
                             '',
                             '*SCALE',
                             '.PARAM scale1=10',
                             '.PARAM scale2=10',
                             '.PARAM scale3=10',
                             '.PARAM scale4=10',
                             '.PARAM scale5=10',
                             '.PARAM scale6=10',
                             '.PARAM scale7=10',
                             '.PARAM scale8=10',
                             '.PARAM scale9=280',
                             '.PARAM scale10=35',
                             '.PARAM scale11=35',
                             '',
                             '*Function',
                             '*********',
                             '*DeltaIb = 1*(exp(a2+(b2*Veb)+(c2*(Veb*Veb))) - exp(a1+(b1*Veb)+(c1*(Veb*Veb))))',
                             '*.func deltaIb(x) {scale*(exp(a2+(b2*x)+(c2*(pow(x,2)))) - exp(a1+(b1*x)+(c1*(pow(x,2)))))}',
                             '*PNP',
                             '.func deltaIb1(x) {scale1*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                             '.func deltaIb2(x) {scale2*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                             '.func deltaIb3(x) {scale3*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                             '.func deltaIb4(x) {scale4*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                             '.func deltaIb5(x) {scale5*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                             '.func deltaIb6(x) {scale6*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                             '',
                             '*NPN',
                             '.func deltaIb7(x) {scale7*((exp(a4+(b4*x)+(c4*(x*x)))) - (exp(a3+(b3*x)+(c3*(x*x)))))}',
                             '.func deltaIb8(x) {scale8*((exp(a4+(b4*x)+(c4*(x*x)))) - (exp(a3+(b3*x)+(c3*(x*x)))))}',
                             '.func deltaIb9(x) {scale9*((exp(a4+(b4*x)+(c4*(x*x)))) - (exp(a3+(b3*x)+(c3*(x*x)))))}',
                             '.func deltaIb10(x) {scale10*((exp(a4+(b4*x)+(c4*(x*x)))) - (exp(a3+(b3*x)+(c3*(x*x)))))}',
                             '.func deltaIb11(x) {scale11*((exp(a4+(b4*x)+(c4*(x*x)))) - (exp(a3+(b3*x)+(c3*(x*x)))))}',
                             '',
                             '*Input',
                             '.dc VIN 0 30 0.01',
                             '',
                             '*Output',
                             '.print dc format=noindex file=' + output_filepath,
                             '+ V(2)',
                             '',
                             '+ I(VOUT)',
                             '*+ {deltaIb1(V(4)-V(8))}',
                             '*+ {deltaIb2(V(4)-V(8))}',
                             '*+ {deltaIb3(V(4)-V(8))}',
                             '*+ {deltaIb4(V(4)-V(8))}',
                             '*+ {deltaIb5(V(3)-V(8))}',
                             '*+ {deltaIb6(V(2)-V(7))}',
                             '+ {deltaIb7(V(6,11))}',
                             '+ V(6,11)',
                             '*+ {deltaIb8(V(1,11))}',
                             '+ V(5,15)',
                             '+ {deltaIb9(V(5,15))}',
                             '*+ {deltaIb10(V(5,12))}',
                             '*+ {deltaIb11(V(5,12))}',
                             '',
                             '*Voltage Controlled Current Source',
                             '**********************************',
                             '*PNP',
                             'B1 4 8 I={deltaIb1(V(4)-V(8))}',
                             'B2 4 8 I={deltaIb2(V(4)-V(8))}',
                             'B3 4 8 I={deltaIb3(V(4)-V(8))}',
                             'B4 4 8 I={deltaIb4(V(4)-V(8))}',
                             'B5 3 8 I={deltaIb5(V(3)-V(8))}',
                             'B6 2 7 I={deltaIb6(V(2)-V(7))}',
                             '*NPN',
                             'B7 6 11 I={deltaIb7(V(6,11))}',
                             'B8 1 11 I={deltaIb8(V(1,11))}',
                             'B9 5 15 I={deltaIb9(V(5,15))}',
                             'B10 5 12 I={deltaIb10(V(5,12))}',
                             'B11 5 12 I={deltaIb11(V(5,12))}',
                             '',
                             '*Capacitance: C<name> <+ node> <- node> [model name] <value> + [IC=<initial value>]',
                             'c1 1 8 26p',
                             '',
                             '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                             'r1 2 4 260',
                             'r2 2 3 1040',
                             'r3 5 16 5000',
                             'r4 11 5 11000',
                             'r5 12 20 146',
                             'r6 15 20 820',
                             '',
                             '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                             'Q1 6 8 4 QLPMOD 10 temp=27',
                             'Q2 6 8 4 QLPMOD 10 temp=27',
                             'Q3 1 8 4 QLPMOD 10 temp=27',
                             'Q4 1 8 4 QLPMOD 10 temp=27',
                             'Q5 8 8 3 QLPMOD 10 temp=27',
                             'Q6 7 7 2 QLPMOD 10 temp=27',
                             'Q7 7 6 11 QNMOD 10 temp=27',
                             'Q8 8 1 11 QNMOD 10 temp=27',
                             'Q9 6 5 15 QNMOD 280 temp=27',
                             'Q10 5 5 12 QNMOD 35 temp=27',
                             'Q11 1 5 12 QNMOD 35 temp=27',
                             '',
                             '*JFET: J<name> <drain> <gate> <source> <model name> [area value]',
                             'J1 8 16 11 NJF_TYP',
                             '',
                             '*Library',
                             '*npn 2e4 off ctp 3b',
                             '.model QNMOD NPN  (',
                             '+ IS     = 1.68208E-16',
                             '+ BF     = 45.95           NF     = 0.986787        VAF    = 345.2016293',
                             '+ IKF    = 0.0229087       NK     = 0.47574         ISE    = 1.122018E-14',
                             '+ NE     = 1.65            BR     = 0.697           NR     = 2',
                             '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                             '+ NC     = 2               RB     = 140.86          IRB    = 1E-3',
                             '+ RBM    = 50              RE     = 2               RC     = 250.75      )',
                             '',
                             '*lpnp 2e4 off ctp 3b',
                             '.model QLPMOD PNP (',
                             '+ IS     = 8.70964E-16',
                             '+ BF     = 264.9           NF     = 0.99            VAF    = 35.8970174',
                             '+ IKF    = 9.549926E-5     NK     = 0.52            ISE    = 5.495409E-14',
                             '+ NE     = 1.42            BR     = 0.697           NR     = 2',
                             '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                             '+ NC     = 2               RB     = 1E3             IRB    = 3.6E-5',
                             '+ RBM    = 100             RE     = 4.096           RC     = 1)',
                             '',
                             '*JFET',
                             '.model NJF_TYP NJF (',
                             '+ VTO = -1.0	BETA = 6.2E-4	LAMBDA = 0.003',
                             '',
                             '+ RD = 0.01      RS = 1e-4',
                             '',
                             '+ CGS = 3E-12    CGD=1.5E-12     IS=5E-10)',
                             '',
                             '*end of the netlist',
                             '.end']
        return content_AD590_ABM

    def content_LT1175(self, TID_level, output_filepath):
        content_LT1175=['Title: LT1175 / Line Regulation / ' + TID_level + ' / T= 300.15K = 27C',
                        '',
                        '*Input Voltage Source',
                        'V2 4 0 DC 0V',
                        '',
                        '*Schematic name: LT1175 core',
                        '****************************',
                        '*Subcircuit',
                        '*X1 VCC VEE VREF',
                        'X1 0 4 5 BG_sc',
                        '',
                        '*X4 V+ V- VCC VEE VO',
                        'X4 6 5 0 4 7 OPAMP_sc',
                        '',
                        '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                        'r1 0 6 350k',
                        'r2 6 1 100k',
                        'rLIM 3 4 0.001',
                        '',
                        '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                        'Q1 1 2 3 QNMOD 1000',
                        'Q2 0 7 2 QNMOD 10',
                        '',
                        '*Input',
                        '.dc V2 0 -20 -0.1',
                        '',
                        '*Output',
                        '.print dc format=noindex file=' + output_filepath,
                        '+ V(4)',
                        '+ V(1)',
                        '',
                        '',
                        '*Schematic name: BG_sc',
                        '**********************',
                        '.subckt BG_sc VCC VEE VREF',
                        '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                        'r1 VCC 1 10k',
                        'r2 1 8 2.93e6',
                        'r3 8 9 109k',
                        'r4 4 VEE 600',
                        'r5 6 VEE 600',
                        '',
                        '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                        'Q1 2 2 VCC QLPMOD 1',
                        'Q2 3 2 1 QLPMOD 1',
                        'Q3 12 5 9 QLPMOD 1',
                        'Q4 11 5 8 QLPMOD 0.1',
                        'Q5 12 12 7 QNMOD 1',
                        'Q6 11 12 7 QNMOD 1',
                        'Q7 VCC 5 7 QNMOD 1',
                        'Q8 3 3 4 QNMOD 1',
                        'Q9 7 3 6 QNMOD 1',
                        '',
                        '*Voltage Controlled Voltage Source: E<name> <+ node> <-node> <+ controlling node> <- controlling node> <gain>',
                        'E1 VCC VREF VCC 5 1',
                        '',
                        '*Independent Current Source: I<name> <+ node> <-node> [[DC] <value>]',
                        'I1 2 0 DC 3.23uA',
                        '',
                        '*end of the BG_sc subcircuit',
                        '.ends BG_sc',
                        '',
                        '',
                        '*Schematic name: OPAMP_sc',
                        '*************************',
                        '.subckt OPAMP_sc V10 V11 VCC VEE VO',
                        '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                        'r1 7 VEE 4.7k',
                        'r2 3 VEE 4.7k',
                        'r3 VO VEE 60k',
                        'r4 11 VEE 60k',
                        '',
                        '*Capacitance: C<name> <+ node> <- node> [model name] <value> + [IC=<initial value>]',
                        'C1 1 9 0.0056p',
                        '',
                        '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                        'Q1 1 11 VEE QNMOD 10',
                        'Q2 VCC 1 VO QNMOD 1',
                        'Q3 VCC 9 11 QNMOD 1',
                        'Q4 9 4 7 QNMOD 1',
                        'Q5 4 4 3 QNMOD 1',
                        'Q6 9 V10 5 QLPMOD 20',
                        'Q7 4 V11 5 QLPMOD 20',
                        'Q8 6 6 VCC QLPMOD 1',
                        'Q9 5 6 VCC QLPMOD 10',
                        'Q10 1 6 VCC QLPMOD 10',
                        '',
                        '*Independent Current Source: I<name> <+ node> <-node> [[DC] <value>]',
                        'I1 6 0 DC 1.4u',
                        '',
                        '*end of the OPAMP_sc subcircuit',
                        '.ends OPAMP_sc',
                        '',
                        '*Library',
                        '********'
                        ]
        content_LT1175.extend(Library.LIBRARY_TID_LEVEL_MODEL[TID_level])
        content_LT1175.extend(['',
                        '*end of the netlist',
                        '.end',
                        ])
        return content_LT1175

    def content_LT1175_ABM(self, TID_level, output_filepath):
        content_LT1175_ABM = ['Title: LT1175 / Line Regulation / ABM / ' + TID_level + ' / T= 300.15K = 27C',
                              '',
                              '*Input Voltage Source',
                              'V2 4 0 DC 0V',
                              '',
                              '*Schematic name: LT1175 core',
                              '****************************',
                              '*Subcircuit',
                              '*X1 VCC VEE VREF',
                              'X1 0 4 5 BG_sc',
                              '',
                              '*X4 V+ V- VCC VEE VO',
                              'X4 6 5 0 4 7 OPAMP_sc',
                              '',
                              '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                              'r1 0 6 350k',
                              'r2 6 1 100k',
                              'rLIM 3 4 0.001',
                              '',
                              '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                              'Q1 1 2 3 QNMOD 1000',
                              'Q2 0 7 2 QNMOD 10',
                              '',
                              '*Parameters',
                              '***********',
                              '*PRE_RAD',
                              '.PARAM a1=-39.30421',
                              '.PARAM b1=48.21879',
                              '.PARAM c1=-15.6477',
                              '']
        content_LT1175_ABM.extend(Library.PARAMETER_TID_LEVEL_SOURCE[TID_level])
        content_LT1175_ABM.extend([
                              '',
                              '*SCALE',
                              '.PARAM scale1=1',
                              '.PARAM scale2=1',
                              '.PARAM scale3=1',
                              '.PARAM scale4=0.1',
                              '',
                              '.PARAM scale6=20',
                              '.PARAM scale7=20',
                              '.PARAM scale8=1',
                              '.PARAM scale9=10',
                              '.PARAM scale10=10',
                              '',
                              '*Function',
                              '*********',
                              '*DeltaIb = 1*(exp(a2+(b2*Veb)+(c2*(Veb*Veb))) - exp(a1+(b1*Veb)+(c1*(Veb*Veb))))',
                              '*.func deltaIb(x) {scale*(exp(a2+(b2*x)+(c2*(pow(x,2)))) - exp(a1+(b1*x)+(c1*(pow(x,2)))))}',
                              '.func deltaIb1(x) {scale1*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                              '.func deltaIb2(x) {scale2*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                              '.func deltaIb3(x) {scale3*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                              '.func deltaIb4(x) {scale4*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                              '',
                              '.func deltaIb6(x) {scale6*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                              '.func deltaIb7(x) {scale7*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                              '.func deltaIb8(x) {scale8*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                              '.func deltaIb9(x) {scale9*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                              '.func deltaIb10(x) {scale10*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                              '',
                              '*Input',
                              '.dc V2 0 -20 -0.1',
                              '',
                              '*Output',
                              '.print dc format=noindex file=' + output_filepath,
                              '+ V(4)',
                              '+ V(1)',
                              '',
                              '',
                              '*Schematic name: BG_sc',
                              '**********************',
                              '.subckt BG_sc VCC VEE VREF',
                              '*Voltage Controlled Current Source BG',
                              'B1 VCC 2 I={deltaIb1(V(VCC)-V(2))}',
                              'B2 1 2 I={deltaIb2(V(1)-V(2))}',
                              'B3 9 5 I={deltaIb3(V(9)-V(5))}',
                              'B4 8 5 I={deltaIb4(V(8)-V(5))}',
                              '',
                              '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                              'r1 VCC 1 10k',
                              'r2 1 8 2.93e6',
                              'r3 8 9 109k',
                              'r4 4 VEE 600',
                              'r5 6 VEE 600',
                              '',
                              '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                              'Q1 2 2 VCC QLPMOD 1',
                              'Q2 3 2 1 QLPMOD 1',
                              'Q3 12 5 9 QLPMOD 1',
                              'Q4 11 5 8 QLPMOD 0.1',
                              'Q5 12 12 7 QNMOD 1',
                              'Q6 11 12 7 QNMOD 1',
                              'Q7 VCC 5 7 QNMOD 1',
                              'Q8 3 3 4 QNMOD 1',
                              'Q9 7 3 6 QNMOD 1',
                              '',
                              '*Voltage Controlled Voltage Source: E<name> <+ node> <-node> <+ controlling node> <- controlling node> <gain>',
                              'E1 VCC VREF VCC 5 1',
                              '',
                              '*Independent Current Source: I<name> <+ node> <-node> [[DC] <value>]',
                              'I1 2 0 DC 3.23uA',
                              '',
                              '*end of the BG_sc subcircuit',
                              '.ends BG_sc',
                              '',
                              '',
                              '*Schematic name: OPAMP_sc',
                              '*************************',
                              '.subckt OPAMP_sc V10 V11 VCC VEE VO',
                              '',
                              '*Voltage Controlled Current Source OPAMP',
                              'B6 5 V10 I={deltaIb6(V(5)-V(V10))}',
                              'B7 5 V11 I={deltaIb7(V(5)-V(V11))}',
                              'B8 6 VCC I={deltaIb8(V(6)-V(VCC))}',
                              'B9 6 VCC I={deltaIb9(V(6)-V(VCC))}',
                              'B10 6 VCC I={deltaIb10(V(6)-V(VCC))}',
                              '',
                              '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                              'r1 7 VEE 4.7k',
                              'r2 3 VEE 4.7k',
                              'r3 VO VEE 60k',
                              'r4 11 VEE 60k',
                              '',
                              '*Capacitance: C<name> <+ node> <- node> [model name] <value> + [IC=<initial value>]',
                              'C1 1 9 0.0056p',
                              '',
                              '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                              'Q1 1 11 VEE QNMOD 10',
                              'Q2 VCC 1 VO QNMOD 1',
                              'Q3 VCC 9 11 QNMOD 1',
                              'Q4 9 4 7 QNMOD 1',
                              'Q5 4 4 3 QNMOD 1',
                              'Q6 9 V10 5 QLPMOD 20',
                              'Q7 4 V11 5 QLPMOD 20',
                              'Q8 6 6 VCC QLPMOD 1',
                              'Q9 5 6 VCC QLPMOD 10',
                              'Q10 1 6 VCC QLPMOD 10',
                              '',
                              '*Independent Current Source: I<name> <+ node> <-node> [[DC] <value>]',
                              'I1 6 0 DC 1.4u',
                              '',
                              '*end of the OPAMP_sc subcircuit',
                              '.ends OPAMP_sc',
                              '',
                              '*Library',
                              '********',
                              '* npn prerad off ctp 3b',
                              '.model QNMOD NPN (',
                              '+ IS = 1.68208E-16',
                              '+ BF = 84.058    NF = 0.986787 VAF = 351.9861415',
                              '+ IKF = 9.86E-3  NK = 0.47574  ISE = 7.1029E-15',
                              '+ NE = 2.06453   BR = 0.697    NR = 2',
                              '+ VAR = 100      IKR = 0.1     ISC = 1E-17',
                              '+ NC = 2         RB = 140.86   IRB = 1E-3',
                              '+ RBM = 50       RE = 2        RC = 250.75)',
                              '',
                              '*lpnp prerad off ctp 3b',
                              '.model QLPMOD PNP (',
                              '+ IS = 8.70964E-16',
                              '+ BF = 786.9		NF = 0.99                           VAF = 36.3423711',
                              '+ IKF = 6.30957E-5       NK = 0.52                           ISE = 9.54993E-17',
                              '+ NE = 1.27089           BR = 0.697                          NR = 2',
                              '+ VAR = 100              IKR = 0.1                           ISC = 1E-17',
                              '+ NC = 2                 RB = 758.578                        IRB = 3.6E-5',
                              '+ RBM = 100              RE = 4.096                           RC = 1)',
                              '',
                              '*end of the netlist',
                              '.end'])
        return content_LT1175_ABM
