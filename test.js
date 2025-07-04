// INTERCEPTOR DE ASISTENCIAS CON RECONOCIMIENTO FACIAL
// Intercepta el botón de entrada/salida y muestra cámara para reconocimiento

console.log("🚀 Iniciando interceptor de asistencias con reconocimiento facial...");

class AttendanceInterceptor {
    constructor() {
        this.isActive = false;
        this.videoElement = null;
        this.canvasElement = null;
        this.modalContainer = null;
        this.stream = null;
        this.attendanceWidget = null;
    }

    // Inicializar el interceptor
    init() {
        console.log("🔧 Inicializando interceptor...");
        
        // Buscar y obtener el widget de asistencias
        this.findAttendanceWidget();
        
        // Interceptar el botón de asistencias
        this.interceptAttendanceButton();
        
        console.log("✅ Interceptor inicializado correctamente");
    }

    // Encontrar el widget de asistencias de Odoo
    findAttendanceWidget() {
        // Buscar en elementos del DOM que contengan el widget
        const attendanceElements = document.querySelectorAll('.o_hr_attendance_kiosk_mode, .o_hr_attendance_my_attendances');
        
        for (let element of attendanceElements) {
            if (element.__widget) {
                this.attendanceWidget = element.__widget;
                console.log("✅ Widget de asistencias encontrado");
                return;
            }
        }
        
        // Método alternativo: buscar en instancias globales
        if (window.odoo && window.odoo.__DEBUG__) {
            // Buscar en widgets activos
            console.log("🔍 Buscando widget en instancias globales...");
        }
        
        console.log("⚠️ Widget de asistencias no encontrado directamente");
    }

    // Interceptar el botón de asistencias
    interceptAttendanceButton() {
        console.log("🎯 Interceptando botón de asistencias...");
        
        // Buscar el botón principal de asistencias
        const attendanceButton = document.querySelector('.o_hr_attendance_sign_in_out_icon');
        
        if (!attendanceButton) {
            console.log("❌ Botón de asistencias no encontrado");
            setTimeout(() => this.interceptAttendanceButton(), 1000);
            return;
        }
        
        // Verificar si ya está interceptado
        if (attendanceButton.hasAttribute('data-facial-intercepted')) {
            console.log("⚠️ Botón ya interceptado");
            return;
        }
        
        console.log("✅ Botón de asistencias encontrado");
        
        // Marcar como interceptado
        attendanceButton.setAttribute('data-facial-intercepted', 'true');
        
        // Guardar el handler original
        const originalHandler = attendanceButton.onclick;
        
        // Reemplazar con nuestro interceptor
        attendanceButton.onclick = (event) => {
            event.preventDefault();
            event.stopPropagation();
            
            console.log("🎯 ¡Botón de asistencias interceptado!");
            
            // Mostrar modal con cámara para reconocimiento
            this.showFacialRecognitionModal(originalHandler);
        };
        
        // Agregar indicador visual
        this.addVisualIndicator();
        
        console.log("🎯 Interceptor configurado exitosamente");
    }

    // Mostrar modal con cámara para reconocimiento facial
    async showFacialRecognitionModal(originalHandler) {
        console.log("� Abriendo modal de reconocimiento facial...");
        
        try {
            // Crear modal
            this.createModal();
            
            // Iniciar cámara
            await this.startCamera();
            
            // Iniciar proceso de reconocimiento
            this.startFacialRecognition(originalHandler);
            
        } catch (error) {
            console.error("❌ Error abriendo modal:", error);
            this.cleanup();
            
            // Ejecutar función original como respaldo
            if (originalHandler) {
                originalHandler();
            }
        }
    }

    // Crear modal visual
    createModal() {
        console.log("🎨 Creando modal visual...");
        
        // Crear contenedor principal
        this.modalContainer = document.createElement('div');
        this.modalContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            font-family: Arial, sans-serif;
        `;
        
        // Crear contenido del modal
        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 500px;
            width: 90%;
        `;
        
        // Título
        const title = document.createElement('h2');
        title.textContent = '👁️ Reconocimiento Facial';
        title.style.cssText = 'margin: 0 0 20px 0; color: #333;';
        
        // Video para mostrar cámara
        this.videoElement = document.createElement('video');
        this.videoElement.autoplay = true;
        this.videoElement.muted = true;
        this.videoElement.playsInline = true;
        this.videoElement.style.cssText = `
            width: 100%;
            max-width: 400px;
            height: 300px;
            border-radius: 10px;
            border: 3px solid #007bff;
            background: #f8f9fa;
            object-fit: cover;
        `;
        
        // Canvas para mostrar detecciones (oculto inicialmente)
        this.canvasElement = document.createElement('canvas');
        this.canvasElement.width = 400;
        this.canvasElement.height = 300;
        this.canvasElement.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            pointer-events: none;
            border-radius: 10px;
        `;
        
        // Contenedor para video y canvas
        const videoContainer = document.createElement('div');
        videoContainer.style.cssText = 'position: relative; display: inline-block;';
        videoContainer.appendChild(this.videoElement);
        videoContainer.appendChild(this.canvasElement);
        
        // Estado del reconocimiento
        this.statusElement = document.createElement('div');
        this.statusElement.style.cssText = `
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            color: #666;
            font-weight: bold;
        `;
        this.statusElement.textContent = '📷 Iniciando cámara...';
        
        // Botón de cancelar
        const cancelButton = document.createElement('button');
        cancelButton.textContent = '❌ Cancelar';
        cancelButton.style.cssText = `
            background: #dc3545;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 15px;
        `;
        cancelButton.onclick = () => this.cleanup();
        
        // Ensamblar modal
        modalContent.appendChild(title);
        modalContent.appendChild(videoContainer);
        modalContent.appendChild(this.statusElement);
        modalContent.appendChild(cancelButton);
        
        this.modalContainer.appendChild(modalContent);
        document.body.appendChild(this.modalContainer);
        
        console.log("✅ Modal creado");
    }

    // Iniciar cámara
    async startCamera() {
        console.log("📹 Iniciando cámara...");
        
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                }
            });
            
            this.videoElement.srcObject = this.stream;
            
            // Esperar a que el video esté listo
            await new Promise((resolve) => {
                this.videoElement.onloadedmetadata = resolve;
            });
            
            this.updateStatus('👀 Cámara activa - Posiciona tu rostro');
            console.log("✅ Cámara iniciada correctamente");
            
        } catch (error) {
            console.error("❌ Error accediendo a la cámara:", error);
            this.updateStatus('❌ Error accediendo a la cámara');
            throw error;
        }
    }

    // Iniciar proceso de reconocimiento facial
    startFacialRecognition(originalHandler) {
        console.log("🧠 Iniciando reconocimiento facial...");
        
        this.updateStatus('🔍 Buscando rostro...');
        
        // Aquí implementaremos la lógica de reconocimiento usando la API del módulo
        this.performFacialRecognition(originalHandler);
    }

    // Realizar reconocimiento facial usando la API del módulo
    async performFacialRecognition(originalHandler) {
        console.log("🎯 Ejecutando reconocimiento facial con API del módulo...");
        
        try {
            // Verificar que Human.js esté disponible
            if (typeof Human === 'undefined') {
                console.log("⚠️ Human.js no disponible, cargando...");
                await this.loadHumanJS();
            }
            
            // Obtener descriptores de empleados
            const employeeDescriptors = await this.loadEmployeeDescriptors();
            
            if (!employeeDescriptors || employeeDescriptors.length === 0) {
                throw new Error("No se encontraron descriptores de empleados");
            }
            
            this.updateStatus('🤖 IA cargada - Analizando rostro...');
            
            // Iniciar detección en tiempo real
            this.startRealTimeDetection(employeeDescriptors, originalHandler);
            
        } catch (error) {
            console.error("❌ Error en reconocimiento facial:", error);
            this.updateStatus('❌ Error en reconocimiento facial');
            
            // Esperar un poco y cerrar
            setTimeout(() => {
                this.cleanup();
                if (originalHandler) originalHandler();
            }, 2000);
        }
    }

    // Cargar Human.js si no está disponible
    async loadHumanJS() {
        console.log("📦 Cargando Human.js...");
        
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = '/hr_attendance_controls_pro/static/src/js/lib/human-1.6.7.js';
            script.onload = () => {
                console.log("✅ Human.js cargado");
                resolve();
            };
            script.onerror = () => {
                reject(new Error("Error cargando Human.js"));
            };
            document.head.appendChild(script);
        });
    }

    // Cargar descriptores de empleados usando la API del módulo
    async loadEmployeeDescriptors() {
        console.log("📋 Cargando descriptores de empleados...");
        
        try {
            const response = await fetch('/hr_attendance_controls_pro/loadLabeledImages/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {},
                    id: Date.now()
                })
            });
            
            const data = await response.json();
            console.log("📦 Respuesta de la API:", data);
            
            if (data.result && data.result.length > 0) {
                console.log(`✅ ${data.result.length} empleados con descriptores cargados`);
                
                // Debug: mostrar información de cada empleado
                data.result.forEach((employee, index) => {
                    console.log(`👤 Empleado ${index + 1}: ${employee.name || employee.label}`);
                    console.log(`📊 Descriptores: ${employee.descriptors ? employee.descriptors.length : 0}`);
                    if (employee.descriptors && employee.descriptors.length > 0) {
                        console.log(`🔍 Primer descriptor (muestra): ${employee.descriptors[0].substring(0, 100)}...`);
                    }
                });
                
                return data.result;
            } else {
                throw new Error("No se encontraron descriptores en la respuesta");
            }
            
        } catch (error) {
            console.error("❌ Error cargando descriptores:", error);
            throw error;
        }
    }

    // Iniciar detección en tiempo real
    startRealTimeDetection(employeeDescriptors, originalHandler) {
        console.log("🔄 Iniciando detección en tiempo real...");
        
        // Configurar Human.js
        const human = new Human.Human({
            modelBasePath: '/hr_attendance_controls_pro/static/src/js/models/',
            face: {
                enabled: true,
                detector: { rotation: false },
                description: { enabled: true },
                mesh: { enabled: false },
                iris: { enabled: false },
                emotion: { enabled: false },
                antispoof: { enabled: false },
                liveness: { enabled: false }
            },
            body: { enabled: false },
            hand: { enabled: false },
            object: { enabled: false }
        });
        
        human.load().then(() => {
            console.log("✅ Human.js configurado y listo");
            this.updateStatus('🎯 Listo - Mira a la cámara');
            
            // Iniciar loop de detección
            this.detectionLoop(human, employeeDescriptors, originalHandler);
        });
    }

    // Loop de detección facial
    async detectionLoop(human, employeeDescriptors, originalHandler) {
        if (!this.videoElement || !this.stream) {
            return; // Modal cerrado
        }
        
        try {
            // Detectar rostros en el video actual
            const result = await human.detect(this.videoElement);
            
            // Limpiar canvas
            const ctx = this.canvasElement.getContext('2d');
            ctx.clearRect(0, 0, this.canvasElement.width, this.canvasElement.height);
            
            if (result.face && result.face.length > 0) {
                const face = result.face[0];
                console.log(`👤 Rostro detectado - Confianza: ${(face.score * 100).toFixed(1)}%`);
                
                // VALIDACIÓN ESTRICTA: Verificar que realmente hay un rostro válido
                if (face.score < 0.8) {
                    console.log(`⚠️ Confianza muy baja (${(face.score * 100).toFixed(1)}%), ignorando detección`);
                    this.updateStatus('👀 Buscando rostro con mejor calidad...');
                    setTimeout(() => this.detectionLoop(human, employeeDescriptors, originalHandler), 200);
                    return;
                }
                
                // Verificar que el rostro tenga un tamaño mínimo razonable
                if (face.box && (face.box.width < 50 || face.box.height < 50)) {
                    console.log(`⚠️ Rostro muy pequeño (${face.box.width}x${face.box.height}), ignorando`);
                    this.updateStatus('👀 Acércate más a la cámara...');
                    setTimeout(() => this.detectionLoop(human, employeeDescriptors, originalHandler), 200);
                    return;
                }
                
                // Dibujar caja del rostro
                this.drawFaceBox(ctx, face);
                
                if (face.embedding && face.embedding.length > 0) {
                    console.log(`🧠 Embedding detectado con ${face.embedding.length} dimensiones`);
                    
                    // VALIDACIÓN DEL EMBEDDING: Verificar que no sea un embedding "vacío" o inválido
                    const nonZeroValues = face.embedding.filter(val => Math.abs(val) > 0.001).length;
                    if (nonZeroValues < face.embedding.length * 0.1) {
                        console.log(`⚠️ Embedding parece inválido (solo ${nonZeroValues} valores no-cero), ignorando`);
                        this.updateStatus('👀 Mejorando calidad de detección...');
                        setTimeout(() => this.detectionLoop(human, employeeDescriptors, originalHandler), 200);
                        return;
                    }
                    
                    // Debug: estadísticas del embedding detectado
                    const min = Math.min(...face.embedding);
                    const max = Math.max(...face.embedding);
                    const avg = face.embedding.reduce((a, b) => a + b, 0) / face.embedding.length;
                    console.log(`📊 Estadísticas embedding: Min=${min.toFixed(3)}, Max=${max.toFixed(3)}, Avg=${avg.toFixed(3)}`);
                    console.log(`📊 Muestra del embedding: [${face.embedding.slice(0, 5).map(v => v.toFixed(3)).join(', ')}...]`);
                    
                    this.updateStatus('🔍 Rostro válido detectado - Identificando...');
                    
                    // Buscar coincidencia con empleados
                    const match = this.findEmployeeMatch(face.embedding, employeeDescriptors);
                    
                    if (match) {
                        console.log(`✅ Empleado identificado: ${match.employee.name || match.employee.label}`);
                        console.log(`🎯 Confianza de detección: ${(face.score * 100).toFixed(1)}%`);
                        console.log(`🎯 Similitud facial: ${match.similarity.toFixed(1)}%`);
                        
                        // VALIDACIÓN FINAL: Solo procesar si ambas métricas son altas
                        if (face.score >= 0.8 && match.similarity >= 80) {
                            this.updateStatus(`✅ ¡Hola ${match.employee.name || match.employee.label}! (${match.similarity.toFixed(1)}%)`);
                            
                            // Procesar asistencia usando la API del módulo
                            await this.processAttendance(match.employee, originalHandler);
                            return; // Salir del loop
                        } else {
                            console.log(`⚠️ Métricas insuficientes - Detección: ${(face.score * 100).toFixed(1)}%, Similitud: ${match.similarity.toFixed(1)}%`);
                            this.updateStatus('🔍 Validando identidad... Mantén la posición');
                        }
                    } else {
                        this.updateStatus('❓ Rostro no reconocido - Sigue intentando...');
                    }
                } else {
                    console.log("⚠️ Rostro detectado pero sin embedding válido");
                    this.updateStatus('⚠️ Rostro detectado pero sin datos suficientes');
                }
            } else {
                this.updateStatus('👀 Buscando rostro...');
            }
            
        } catch (error) {
            console.error("❌ Error en detección:", error);
            this.updateStatus('❌ Error en detección facial');
        }
        
        // Continuar loop
        setTimeout(() => this.detectionLoop(human, employeeDescriptors, originalHandler), 200);
    }

    // Dibujar caja del rostro en el canvas
    drawFaceBox(ctx, face) {
        const box = face.box;
        
        // Ajustar coordenadas al tamaño del canvas
        const scaleX = this.canvasElement.width / this.videoElement.videoWidth;
        const scaleY = this.canvasElement.height / this.videoElement.videoHeight;
        
        const x = box.x * scaleX;
        const y = box.y * scaleY;
        const width = box.width * scaleX;
        const height = box.height * scaleY;
        
        // Dibujar caja
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, width, height);
        
        // Dibujar puntos clave si están disponibles
        if (face.keypoints) {
            ctx.fillStyle = '#00ff00';
            face.keypoints.forEach(point => {
                ctx.beginPath();
                ctx.arc(point.x * scaleX, point.y * scaleY, 2, 0, 2 * Math.PI);
                ctx.fill();
            });
        }
    }

    // Encontrar coincidencia de empleado
    findEmployeeMatch(faceDescriptor, employeeDescriptors) {
        let bestMatch = null;
        let bestSimilarity = 0;
        
        console.log(`🔍 Comparando descriptor detectado (${faceDescriptor.length} dimensiones) con ${employeeDescriptors.length} empleados`);
        
        for (const employee of employeeDescriptors) {
            console.log(`👤 Verificando empleado: ${employee.name || employee.label}`);
            
            for (const descriptorStr of employee.descriptors) {
                try {
                    let storedDescriptor;
                    
                    console.log(`📊 Procesando descriptor de longitud: ${descriptorStr.length}`);
                    
                    // Parsear descriptor (puede estar en JSON o base64)
                    if (descriptorStr.startsWith('[')) {
                        // Formato JSON
                        storedDescriptor = JSON.parse(descriptorStr);
                        console.log(`✅ Descriptor JSON parseado: ${storedDescriptor.length} dimensiones`);
                    } else {
                        // Formato base64 - decodificación mejorada
                        try {
                            const binaryString = atob(descriptorStr);
                            const bytes = new Uint8Array(binaryString.length);
                            
                            for (let i = 0; i < binaryString.length; i++) {
                                bytes[i] = binaryString.charCodeAt(i);
                            }
                            
                            console.log(`🔧 Bytes decodificados: ${bytes.length}`);
                            
                            // Convertir bytes a Float32Array
                            const floatArray = new Float32Array(bytes.buffer);
                            storedDescriptor = Array.from(floatArray);
                            
                            console.log(`✅ Descriptor base64 decodificado: ${storedDescriptor.length} dimensiones`);
                            
                            // Verificar que los valores sean válidos
                            const validValues = storedDescriptor.filter(val => !isNaN(val) && isFinite(val));
                            if (validValues.length !== storedDescriptor.length) {
                                console.log(`⚠️ Descriptor contiene valores inválidos: ${validValues.length}/${storedDescriptor.length} válidos`);
                                continue;
                            }
                            
                            // Debug: mostrar estadísticas del descriptor
                            const min = Math.min(...storedDescriptor);
                            const max = Math.max(...storedDescriptor);
                            const avg = storedDescriptor.reduce((a, b) => a + b, 0) / storedDescriptor.length;
                            console.log(`📊 Estadísticas descriptor: Min=${min.toFixed(3)}, Max=${max.toFixed(3)}, Avg=${avg.toFixed(3)}`);
                            
                        } catch (b64Error) {
                            console.log(`❌ Error decodificando base64: ${b64Error.message}`);
                            continue;
                        }
                    }
                    
                    if (storedDescriptor && storedDescriptor.length === faceDescriptor.length) {
                        const similarity = this.calculateSimilarity(faceDescriptor, storedDescriptor);
                        console.log(`🎯 Similitud calculada: ${(similarity * 100).toFixed(2)}%`);
                        
                        if (similarity > bestSimilarity && similarity > 0.2) { // Reducir umbral a 20%
                            bestSimilarity = similarity;
                            bestMatch = {
                                employee: employee,
                                similarity: similarity * 100,
                                descriptor: storedDescriptor
                            };
                            console.log(`🏆 Nueva mejor coincidencia: ${(similarity * 100).toFixed(2)}%`);
                        }
                    } else if (storedDescriptor) {
                        console.log(`⚠️ Dimensiones no coinciden: detector=${faceDescriptor.length}, almacenado=${storedDescriptor.length}`);
                    }
                    
                } catch (error) {
                    console.log(`❌ Error procesando descriptor: ${error.message}`);
                    continue;
                }
            }
        }
        
        if (bestMatch) {
            console.log(`✅ Mejor coincidencia encontrada: ${bestMatch.employee.name || bestMatch.employee.label} con ${bestMatch.similarity.toFixed(2)}%`);
        } else {
            console.log(`❌ No se encontró ninguna coincidencia válida`);
        }
        
        return bestMatch;
    }

    // Calcular similitud entre descriptores usando distancia coseno
    calculateSimilarity(desc1, desc2) {
        if (desc1.length !== desc2.length) {
            return 0;
        }
        
        // Calcular similitud coseno (más apropiada para embeddings faciales)
        let dotProduct = 0;
        let norm1 = 0;
        let norm2 = 0;
        
        for (let i = 0; i < desc1.length; i++) {
            dotProduct += desc1[i] * desc2[i];
            norm1 += desc1[i] * desc1[i];
            norm2 += desc2[i] * desc2[i];
        }
        
        const magnitude1 = Math.sqrt(norm1);
        const magnitude2 = Math.sqrt(norm2);
        
        if (magnitude1 === 0 || magnitude2 === 0) {
            return 0;
        }
        
        const cosineSimilarity = dotProduct / (magnitude1 * magnitude2);
        
        // Convertir de [-1, 1] a [0, 1]
        const normalizedSimilarity = (cosineSimilarity + 1) / 2;
        
        // También calcular distancia euclidiana para comparación
        let euclideanSum = 0;
        for (let i = 0; i < desc1.length; i++) {
            const diff = desc1[i] - desc2[i];
            euclideanSum += diff * diff;
        }
        const euclideanDistance = Math.sqrt(euclideanSum);
        const euclideanSimilarity = Math.max(0, 1 - (euclideanDistance / Math.sqrt(desc1.length * 4))); // Normalizar por dimensión
        
        console.log(`📐 Distancia euclidiana: ${euclideanDistance.toFixed(4)}, Similitud euclidiana: ${(euclideanSimilarity * 100).toFixed(2)}%`);
        console.log(`🎯 Similitud coseno: ${cosineSimilarity.toFixed(4)}, Normalizada: ${(normalizedSimilarity * 100).toFixed(2)}%`);
        
        // Usar la mejor de las dos métricas
        const finalSimilarity = Math.max(normalizedSimilarity, euclideanSimilarity);
        
        console.log(`🏆 Similitud final: ${(finalSimilarity * 100).toFixed(2)}%`);
        
        return finalSimilarity;
    }

    // Procesar asistencia usando la API del módulo
    async processAttendance(employee, originalHandler) {
        console.log(`📝 Procesando asistencia para: ${employee.name}`);
        this.updateStatus('📝 Registrando asistencia...');
        
        try {
            // Usar la función del widget de asistencias si está disponible
            if (this.attendanceWidget && this.attendanceWidget.update_attendance) {
                // Simular que el empleado identificado es el usuario actual
                this.attendanceWidget.data_employee_id = employee.label;
                this.attendanceWidget.update_attendance();
            } else {
                // Usar método directo
                await this.registerAttendanceDirect(employee.label);
            }
            
            this.updateStatus('✅ Asistencia registrada exitosamente');
            
            // Cerrar modal después de un momento
            setTimeout(() => {
                this.cleanup();
            }, 2000);
            
        } catch (error) {
            console.error("❌ Error registrando asistencia:", error);
            this.updateStatus('❌ Error registrando asistencia');
            
            // Intentar con método original
            setTimeout(() => {
                this.cleanup();
                if (originalHandler) originalHandler();
            }, 2000);
        }
    }

    // Registrar asistencia directamente
    async registerAttendanceDirect(employeeId) {
        const response = await fetch('/web/dataset/call_kw', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'call',
                params: {
                    model: 'hr.employee',
                    method: 'attendance_manual',
                    args: [[parseInt(employeeId)], 'hr_attendance.hr_attendance_action_my_attendances'],
                    kwargs: {}
                },
                id: Date.now()
            })
        });
        
        const result = await response.json();
        
        if (result.error) {
            throw new Error(result.error.data.message);
        }
        
        return result.result;
    }

    // Actualizar estado visual
    updateStatus(message) {
        if (this.statusElement) {
            this.statusElement.textContent = message;
            console.log(`📱 ${message}`);
        }
    }

    // Agregar indicador visual de que el interceptor está activo
    addVisualIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'facial-interceptor-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(45deg, #28a745, #20c997);
            color: white;
            padding: 10px 15px;
            border-radius: 25px;
            font-size: 12px;
            z-index: 8888;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            font-family: Arial, sans-serif;
            pointer-events: none;
        `;
        indicator.textContent = '👁️ Reconocimiento Facial Activo';
        document.body.appendChild(indicator);
    }

    // Limpiar recursos
    cleanup() {
        console.log("🧹 Limpiando recursos...");
        
        // Detener stream de video
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        // Remover modal
        if (this.modalContainer) {
            this.modalContainer.remove();
            this.modalContainer = null;
        }
        
        // Limpiar referencias
        this.videoElement = null;
        this.canvasElement = null;
        this.statusElement = null;
        
        console.log("✅ Recursos limpiados");
    }
}

// Crear instancia global y ejecutar
const interceptor = new AttendanceInterceptor();

// Auto-inicializar cuando la página esté lista
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => interceptor.init());
} else {
    interceptor.init();
}

// Exportar para uso manual
window.facialInterceptor = interceptor;

console.log("🎯 Interceptor listo. Haz click en el botón de asistencias para usar reconocimiento facial.");
